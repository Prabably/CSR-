#!/usr/bin/env python3
"""Command line entry point for the reusable paper review skill."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make the checkout importable when this file is executed directly from any
# working directory (the normal documented invocation).
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from paper_review.review import review_file, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="检查论文结构、引用和常见待修改项")
    parser.add_argument("--input", required=True, type=Path, help="论文文件：.md、.txt、.tex 或 .docx")
    parser.add_argument("--output", type=Path, help="Markdown 报告路径")
    parser.add_argument("--json-output", type=Path, help="JSON 报告路径")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.input.is_file():
        print(f"输入文件不存在：{args.input}", file=sys.stderr)
        return 2
    if not args.output and not args.json_output:
        print("请至少提供 --output 或 --json-output", file=sys.stderr)
        return 2
    try:
        report = review_file(args.input)
        write_report(report, args.output, args.json_output)
    except (OSError, UnicodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"已生成报告：{args.output or args.json_output}")
    print(f"状态：{report['status']}；发现 {len(report['findings'])} 项需处理")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
