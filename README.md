# CSR-
提供综述 论文的修改审查意见

## 论文审查 Skill

仓库现在包含一个可迁移的论文文本检查工作流。使用 [SKILL.md](SKILL.md) 查看完整约定，并运行：

```bash
python3 scripts/review_paper.py \
  --input path/to/manuscript.md \
  --output artifacts/review.md \
  --json-output artifacts/review.json
```

它会检查常见章节、引用与参考文献对应关系、占位符、摘要长度和过长段落。报告用于辅助修改，不能替代人工学术审查。
