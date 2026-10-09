---
name: paper-review
description: 检查论文结构、引用一致性、占位符和段落可读性，并生成可审阅的修改建议报告。
---

# 论文修改审查 Skill

这个 Skill 用于把论文初稿转换成结构化的检查报告。它适合在正式人工审稿前发现可重复、可解释的文本问题，不能代替同行评议、事实核验、统计复核或学术伦理审查。

## 快速使用

在仓库根目录运行：

```bash
python3 scripts/review_paper.py \
  --input path/to/manuscript.md \
  --output artifacts/review.md \
  --json-output artifacts/review.json
```

支持 Markdown、纯文本、LaTeX 和 DOCX。PDF 请先导出为其中一种格式，以避免依赖不透明的 PDF 解析器。

## 标准工作流

1. 保留原始论文文件，先运行命令生成 Markdown 和 JSON 两份报告。
2. 先处理 `error`，再处理 `warning`；报告中的每项建议都应回到原文核对。
3. 对摘要、方法、结果、讨论和结论做人工学术判断，确认自动检查没有误报。
4. 修改论文后重新运行，并比较两次 JSON 中的 `status`、`metrics` 和 `findings`。
5. 提交前保留报告作为审阅记录，但不要把自动检查结果表述成论文已经通过同行评议。

## 检查内容

- 识别摘要、引言、方法、结果、讨论、结论和参考文献标题。
- 统计词数、中文字符、段落、引用和参考文献数量。
- 检查数字型引用是否能在编号参考文献中找到。
- 检查过长段落和常见占位符，例如 `TODO`、`FIXME`、`TBD`、`???`。
- 对过短摘要和正文缺少引用给出可解释的修改建议。

## 可复用约定

- 输入文件和输出报告使用 UTF-8。
- 生成物放到 `artifacts/` 或其他被 `.gitignore` 忽略的目录，不覆盖原稿。
- 该实现只使用 Python 标准库；新机器只需 Python 3.10 或更高版本。
- 未来扩展期刊格式检查时，应把规则加入 `paper_review/review.py`，并保持 JSON 字段向后兼容。
