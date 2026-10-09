---
name: academic-paper-review
description: Strictly audit, revise, and structure Chinese or English academic papers, reviews, theses, and manuscript sections for scientific logic, evidence boundaries, citation matching, terminology, section purpose, CSR-level synthesis, and length control.
metadata:
  short-description: Strict academic manuscript and review audit
---

# Academic Paper Review

Use this skill whenever the user asks to check, review, audit, polish, compress, or
restructure an academic paper, review article, thesis chapter, manuscript section,
figure explanation, or reference-supported scientific prose. It applies to ordinary
research papers as well as review articles; for reviews, apply the CSR/Nature-level
framework in the review-specific section below.

The user's attached Chinese review command is the governing local checklist. Use the
condensed, non-duplicative version in `references/strict-checklist.md`; preserve the
user's intent but do not treat the command as evidence for scientific facts.

## Non-negotiable review stance

- Do not flatter or merely confirm the author's view. Test it and state concrete
  problems even when the prose is generally strong.
- Classify every material problem as fact, evidence, logic, structure, wording,
  citation boundary, concept, terminology, review positioning, CSR framework, or
  section-proportion issue.
- If a paragraph has no material issue under the requested scope, explicitly state:
  `本段未发现上述问题。`
- Never invent citations, data, mechanisms, experimental conditions, or author intent.
  When a source has not been verified, mark it as unverified and narrow the claim.
- Preserve uncertainty. Separate a reported fact, a mechanism supported by
  characterization, and the review author's inference.

## Required audit order

1. Identify the document type, target section, central scientific question, and
   requested scope. If the user has supplied a custom checklist, read it fully before
   judging the text.
2. Check section positioning: what problem does the section solve, and does every
   paragraph serve that problem rather than a neighboring section's function?
3. Check paragraph purpose and first-sentence centrality. Each paragraph should follow
   the useful sequence: central claim -> mechanism -> representative evidence -> what
   the case supports -> limitation or significance.
4. Check sentence-to-sentence and paragraph-to-paragraph transitions, causal claims,
   comparisons, conditions, and whether the next paragraph responds to the previous
   one.
5. Check evidence strength against the measurement method and source. Do not infer a
   bulk or atomic-scale mechanism from a surface or morphology-only measurement.
6. Check citation-to-claim matching, citation order, citation density, and whether a
   reference supports a fact, a mechanism, a limitation, or only a general principle.
7. Check terminology, abbreviations, chemical formulae, units, and consistency across
   the supplied text and surrounding section.
8. Check length and proportion only after logic and evidence: compress repetition and
   database-like parameter lists, but do not delete a case that performs a distinct
   evidentiary role without telling the user why.

## Evidence boundaries

Use wording proportional to evidence: `表明/报告` for direct observations,
`支持/提示` for supported interpretations, and `可能/推测/尚需验证` for bounded
inference. In particular:

- SEM mainly supports morphology, particle size, cracks, pores, and aggregation; it
  does not by itself prove chemical composition, crystal structure, or bond breaking.
- XRD supports crystalline-phase identification and phase/ordering changes; it does
  not by itself prove a complete reaction path, every intermediate, or atomic-scale
  mechanism.
- XPS reports surface composition, valence, and chemical environment; it does not
  directly represent the bulk.
- FTIR/Raman support functional-group, bonding-environment, or coordination changes;
  they do not alone establish a full reaction pathway.
- ICP or solution analysis supports concentrations, recovery, co-leaching, and
  element distribution; increased target-element leaching is not by itself improved
  selectivity or a mechanism.

## Review-article and CSR-level rules

Treat a review as a synthesis of field knowledge, not a sequence of `A studied... B
reported...` summaries. Determine whether the article is primarily a literature,
technology, mechanism, or conceptual review, and say what prevents it from reaching a
higher level if relevant. For each subsection, build an explicit chain:

`scientific problem -> regulating strategy -> mechanism -> evidence -> performance ->
boundary -> design principle or open question`.

Unify evaluation dimensions across methods. In resource-recovery and pretreatment
sections, distinguish target-element release, selectivity, impurity migration,
mechanism evidence, downstream separation burden, energy/reagent demand, and scale-up
potential. Never equate release enhancement with selectivity improvement, performance
with mechanistic proof, or a single-process result with a general field trend.

Use the `known -> unknown -> significance/future need` pattern in subsection summaries.
Do not create a second highest-level summary that merely repeats the first. Do not
attribute the review author's analytical question to the cited paper unless the paper
actually had that objective; use formulations such as `从……角度看`, `提供……证据`, or
`进一步体现` when reinterpreting a study.

For pretreatment and solid-state-control chapters, explicitly distinguish:

- mechanical input: particle-size change, grain refinement, grain boundaries,
  defects, disorder, and mechanical activation;
- reagent-induced transformation: altered composition, chemical state, intermediate
  phases, sulfate/chloride/nitrate/alkali conversion;
- thermal phase transformation: heating history, temperature, atmosphere, oxidation,
  decomposition, reconstruction, and phase selection.

State whether the evidence establishes reactivity/release, selectivity, or both. Treat
ultrasound, microwave, coupled heating, and mechanochemical leaching according to the
actual stage at which they are applied and whether independent before/after solid-state
evidence exists.

## Output contract

Unless the user requests a different format, report:

1. current problems, grouped by problem type and severity;
2. the governing revision principle and why it is needed;
3. a complete replacement passage when the user asks for revision;
4. citation-placement and evidence-boundary notes;
5. a final check for new problems introduced by the revision, including length and
   section-proportion effects.

When counting length, state the metric used (raw characters, characters excluding
whitespace, Chinese characters, or word-processor word count). Do not call a section
too long without considering its role, evidence density, neighboring-section balance,
and the user's venue or total-manuscript limit.

Keep original and revised text conceptually distinct. Explain non-obvious edits so the
author can verify them; do not silently change scientific scope, citation identity, or
experimental meaning.


