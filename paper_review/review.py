"""Extract and review common manuscript quality signals.

The module intentionally uses only the Python standard library so it can run in a
fresh Codex environment without a package installation step.
"""

from __future__ import annotations

import json
import re
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


REQUIRED_SECTIONS = {
    "abstract": ("摘要", "abstract"),
    "introduction": ("引言", "绪论", "背景", "introduction", "background"),
    "methods": ("方法", "方法学", "实验设计", "materials and methods", "methodology", "methods"),
    "results": ("结果", "实验结果", "results", "findings"),
    "discussion": ("讨论", "discussion"),
    "conclusion": ("结论", "结语", "conclusion", "conclusions"),
    "references": ("参考文献", "参考资料", "references", "bibliography"),
}

PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\?{3,}|待补充|待确认|此处添加", re.I)
NUMERIC_CITATION_RE = re.compile(r"\[(\d+(?:\s*[-,]\s*\d+)*)\]")
AUTHOR_YEAR_RE = re.compile(r"\b[A-Z][A-Za-z-]{2,}(?:\s+et al\.)?\s*[,（(]\s*20\d{2}")
WORD_RE = re.compile(r"[\w'-]+", re.UNICODE)
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
HEADING_RE = re.compile(r"^\s*(?:#{1,6}\s+|(?:\\section|\\subsection)\*?\{)(.+?)(?:\}\s*)?$", re.I)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    title: str
    detail: str
    recommendation: str


def read_manuscript(path: Path) -> str:
    """Read Markdown, text, LaTeX, or a DOCX document as plain text."""
    suffix = path.suffix.lower()
    if suffix == ".docx":
        try:
            with zipfile.ZipFile(path) as archive:
                xml = archive.read("word/document.xml")
        except (KeyError, zipfile.BadZipFile) as exc:
            raise ValueError(f"无法读取 DOCX 文件：{path}") from exc
        root = ElementTree.fromstring(xml)
        text = " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))
        return text
    if suffix in {".md", ".markdown", ".txt", ".text", ".tex", ".latex"} or not suffix:
        return path.read_text(encoding="utf-8-sig")
    if suffix == ".pdf":
        raise ValueError("暂不直接解析 PDF；请先导出为 DOCX、Markdown、LaTeX 或纯文本。")
    raise ValueError(f"不支持的文件类型：{suffix}。支持 .md、.txt、.tex 和 .docx。")


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def _units(text: str) -> int:
    """Count Latin words and CJK characters without collapsing Chinese text."""
    cjk_count = len(CJK_RE.findall(text))
    latin_words = len(_words(CJK_RE.sub(" ", text)))
    return cjk_count + latin_words


def _heading_name(raw: str) -> str:
    return re.sub(r"[*_`:#{}]", " ", raw).strip().lower()


def extract_sections(text: str) -> dict[str, str]:
    """Split a manuscript by common Markdown/LaTeX headings."""
    lines = text.splitlines()
    sections: dict[str, list[str]] = {"front_matter": []}
    current = "front_matter"
    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            heading = _heading_name(match.group(1))
            current = heading or "unnamed_section"
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return {
        name: "\n".join(body).strip()
        for name, body in sections.items()
        if any(line.strip() for line in body)
    }


def _find_section(sections: dict[str, str], aliases: Iterable[str]) -> str | None:
    aliases = tuple(alias.lower() for alias in aliases)
    for name in sections:
        normalized = re.sub(r"\s+", " ", name.lower()).strip()
        if any(alias == normalized or alias in normalized for alias in aliases):
            return name
    return None


def _reference_entries(reference_text: str) -> list[str]:
    return [line.strip() for line in reference_text.splitlines() if line.strip()]


def inspect_manuscript(text: str, source: str) -> dict:
    sections = extract_sections(text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    cjk_chars = len(CJK_RE.findall(text))
    findings: list[Finding] = []
    section_map: dict[str, str | None] = {}

    for key, aliases in REQUIRED_SECTIONS.items():
        found = _find_section(sections, aliases)
        section_map[key] = found
        if found is None:
            severity = "warning" if key in {"discussion", "methods"} else "error"
            findings.append(Finding(
                severity, f"missing-{key}", f"缺少{key}部分",
                f"未识别到常见的 {key} 标题。",
                f"补充明确的 {key} 小节，或使用 README 中约定的标题别名。",
            ))

    abstract_name = section_map["abstract"]
    abstract_words = _units(sections.get(abstract_name or "", ""))
    if abstract_name and abstract_words < 80:
        findings.append(Finding(
            "warning", "short-abstract", "摘要信息密度偏低",
            f"摘要约 {abstract_words} 个词，低于 80 词的最低检查阈值。",
            "在摘要中交代研究问题、方法、核心结果和结论，避免只写背景。",
        ))

    reference_name = section_map["references"]
    reference_text = sections.get(reference_name or "", "")
    references = _reference_entries(reference_text)
    citation_numbers = {int(n) for group in NUMERIC_CITATION_RE.findall(text) for n in re.findall(r"\d+", group)}
    numbered_refs = {int(n) for line in references for n in re.findall(r"^\[?(\d+)\]?", line)}
    text_units = _units(text)
    if text_units > 250 and not citation_numbers and not AUTHOR_YEAR_RE.search(text):
        findings.append(Finding(
            "warning", "no-citations", "正文未识别到引用",
            "正文超过 250 个词，但没有识别到数字型或作者-年份型引用。",
            "为关键论断添加可追溯引用，并确保引用格式与目标期刊一致。",
        ))
    missing_refs = sorted(citation_numbers - numbered_refs) if numbered_refs else []
    if missing_refs:
        findings.append(Finding(
            "error", "unresolved-citations", "存在未匹配的数字引用",
            f"正文引用编号 {', '.join(map(str, missing_refs))} 未在参考文献中找到。",
            "补齐参考文献条目或修正正文中的引用编号。",
        ))

    long_paragraphs = [_units(p) for p in paragraphs if _units(p) > 180]
    if long_paragraphs:
        findings.append(Finding(
            "warning", "long-paragraphs", "段落过长",
            f"发现 {len(long_paragraphs)} 个超过 180 词的段落，最长约 {max(long_paragraphs)} 词。",
            "按论点拆分段落，并让每段首句明确主题。",
        ))
    placeholder_matches = sorted(set(PLACEHOLDER_RE.findall(text)), key=str.lower)
    if placeholder_matches:
        findings.append(Finding(
            "error", "placeholders", "文稿仍含占位符",
            "识别到：" + ", ".join(placeholder_matches),
            "提交前替换占位内容，并重新检查表格、图注和补充材料。",
        ))

    findings.sort(key=lambda item: {"error": 0, "warning": 1, "info": 2}[item.severity])
    return {
        "source": source,
        "metrics": {
            "word_count": text_units,
            "cjk_character_count": cjk_chars,
            "paragraph_count": len(paragraphs),
            "section_count": len(sections),
            "reference_count": len(references),
            "citation_count": len(citation_numbers) or len(AUTHOR_YEAR_RE.findall(text)),
        },
        "sections": section_map,
        "findings": [asdict(finding) for finding in findings],
        "status": "needs_revision" if findings else "ready_for_editorial_review",
    }


def render_markdown(report: dict) -> str:
    metrics = report["metrics"]
    lines = [
        f"# 论文检查报告：{report['source']}",
        "",
        f"状态：`{report['status']}`",
        "",
        "## 统计",
        "",
        f"- 总词数：{metrics['word_count']}",
        f"- 中文字符数：{metrics['cjk_character_count']}",
        f"- 段落数：{metrics['paragraph_count']}",
        f"- 识别到的参考文献：{metrics['reference_count']}",
        f"- 识别到的引用：{metrics['citation_count']}",
        "",
        "## 结构识别",
        "",
    ]
    for key, name in (("abstract", "摘要"), ("introduction", "引言"), ("methods", "方法"), ("results", "结果"), ("discussion", "讨论"), ("conclusion", "结论"), ("references", "参考文献")):
        lines.append(f"- {name}：{'已识别（' + report['sections'][key] + '）' if report['sections'][key] else '未识别'}")
    lines.extend(["", "## 修改建议", ""])
    if not report["findings"]:
        lines.append("未发现自动检查问题。请继续进行人工学术判断和目标期刊格式核对。")
    else:
        for index, finding in enumerate(report["findings"], 1):
            lines.extend([
                f"### {index}. [{finding['severity']}] {finding['title']}",
                "",
                finding["detail"],
                "",
                f"建议：{finding['recommendation']}",
                "",
            ])
    lines.extend(["## 使用边界", "", "这是结构和文本信号检查，不替代同行评议、事实核验、统计复核或学术伦理审查。", ""])
    return "\n".join(lines)


def review_file(path: Path) -> dict:
    text = read_manuscript(path)
    return inspect_manuscript(text, path.name)


def write_report(report: dict, output: Path | None, json_output: Path | None) -> None:
    if output:
        output.write_text(render_markdown(report), encoding="utf-8")
    if json_output:
        json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
