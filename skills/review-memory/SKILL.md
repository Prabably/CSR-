---
name: review-memory
description: Apply the user's durable collaboration and academic-writing lessons before continuing recurring work, revising review chapters, handling citations or Zotero, or fixing a previously corrected pattern.
metadata:
  short-description: Recall user rules and prevent repeated mistakes
---

# Review memory

Use this skill when work depends on the user's prior corrections, recurring writing preferences, literature-review workflow, Zotero handling, or when the user asks to continue earlier work.

## Before work

1. Read the durable lesson file at `C:\Users\污狐狸  九喇嘛\Documents\Codex\memory\CODEX_LESSONS.md` when running locally. In a project checkout, also look for `memory/CODEX_LESSONS.md` at the repository root. If neither is available, say so plainly when relevant and use only context actually present in the conversation.
2. Retrieve specific prior conversation details only when the current task depends on them. A memory summary is a pointer to preferences, not proof of a paper's results or a substitute for source documents.
3. Identify the user's requested deliverable and format. If the user asks for text in chat, provide the text directly in chat. Do not create a PDF or local document unless requested.

## For academic review writing

- State the paragraph's central claim clearly and early. Each paragraph must have a distinct argumentative role and connect evidence to that claim.
- Write review prose, not presentation notes. Avoid flowchart-like chains, pseudo-equations made from concepts, slide-style boxed phrases, and routine numbered points in prose. Use lists only when the document's genre or a genuine taxonomy calls for them.
- Prefer confident, evidence-led synthesis. Keep necessary evidence boundaries, but remove repetitive caveats, defensive narration, and self-undermining language that does not change the scientific interpretation.
- Keep mechanism claims proportional to source evidence. Distinguish reported performance, direct characterization, mechanistic interpretation, and review-level inference without turning each sentence into a disclaimer.
- Do not re-explain abbreviations or characterization methods already established earlier in the same manuscript unless needed for clarity.
- When revising one section after a user flags a structural or tonal problem, inspect sibling sections for the same pattern and correct the full affected scope.
- Preserve established reference numbering. Continue new references from the project's verified last number; never guess the numbering state.
- For literature claims, prioritize suitable high-quality primary sources and relevant authoritative reviews. Verify bibliographic details and the full text when making source-specific scientific claims. Separate real-waste studies from model systems and performance-only evidence from mechanistic evidence.

## Learning from correction

When the user corrects an output:

1. Apply the correction to the requested material and inspect nearby material for the same failure mode.
2. Convert durable feedback into a short rule with three parts: failure pattern, desired behavior, and a check that catches recurrence.
3. Add or refine one lesson in `memory/CODEX_LESSONS.md` (project copy) and, when relevant to all local conversations, the user memory file under `Documents\Codex\memory`.
4. Avoid duplicate rules, overgeneralization, and claims that the file makes future errors impossible. It improves recall and provides a concrete review check; it is not model retraining.

## Cloud task boundary

Cloud tasks can use this skill and memory only when the task environment or connected repository contains them. Do not claim local user-level rules, Zotero databases, browser sessions, or other files were loaded unless verified in that environment. If the project copy is present, use it as the source of truth for that task.

