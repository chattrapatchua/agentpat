---
name: rule-creator
description: "Scan installed skills for cross-cutting principles and distill them into rules—append, revise, or create rule files."
origin: ECC
---

# Rule Creator

Scan installed skills, extract general principles that appear in multiple skills, and distill them into rules—by appending to existing rule files, revising outdated content, or creating new rule files.

Follow **deterministic collection + LLM judgment**: scripts gather facts exhaustively; the LLM reads full context and decides.

## When to use

* Periodic rule maintenance (monthly or after installing new skills)
* After a skill inventory, when patterns should become rules
* When rules feel incomplete relative to the skills you actually use

## How it works

The Rule Creator workflow has three phases:

### Phase 1: Inventory (deterministic collection)

#### 1a. Collect skill list

```bash
bash ~/.cursor/skills/rule-creator/scripts/scan-skills.sh
```

#### 1b. Collect rules index

```bash
bash ~/.cursor/skills/rule-creator/scripts/scan-rules.sh
```

#### 1c. Present to the user

```
Rule Creator — Phase 1: Inventory
────────────────────────────────────────
Skills: scanned {N} files
Rules: indexed {M} files ({K} headings)

Cross-reading analysis in progress...
```

### Phase 2: Read, match, and decide (LLM judgment)

Extraction and matching happen in one pass. Rule files are small enough (~800 lines total) to provide full text to the LLM—no grep pre-filtering.

#### Batch processing

Group skills into **theme clusters** from their descriptions. Analyze each cluster in a subagent with the full rules text.

#### Cross-batch merge

After all batches finish, merge candidate rules:

* Deduplicate candidates with the same or overlapping principles
* Re-check the **2+ skills** requirement using **combined** evidence from all batches—a principle seen in only one skill per batch but in 2+ skills overall is valid

#### Subagent prompt

Launch a general-purpose agent with:

````
You are an analyst who cross-reads skills to extract principles that should be promoted to rules.

## Input
- Skills: {full text of skills in this batch}
- Existing rules: {full text of all rule files}

## Extraction criteria

Include a candidate principle **only** when **all** of the following hold:

1. **Appears in 2+ skills**: principles that appear in only one skill stay in that skill
2. **Actionable behavior change**: expressible as "Do X" or "Do not Y"—not "X is important"
3. **Clear violation risk**: one sentence on what goes wrong if the principle is ignored
4. **Not already in rules**: check all rule text—including the same idea under different wording

## Match and verdict

For each candidate, compare against all rules and assign a verdict:

- **Append**: add to an existing section in an existing rule file
- **Revise**: existing rule text is wrong or insufficient—propose a fix
- **New Section**: add a new section in an existing rule file
- **New File**: create a new rule file
- **Already Covered**: rules already cover it (even if wording differs)
- **Too Specific**: keep at skill level

## Output format (per candidate)

```json
{
  "principle": "1–2 sentences in 'Do X' / 'Do not Y' form",
  "evidence": ["skill-name: §section", "skill-name: §section"],
  "violation_risk": "one sentence",
  "verdict": "Append / Revise / New Section / New File / Already Covered / Too Specific",
  "target_rule": "filename §section, or 'new'",
  "confidence": "high / medium / low",
  "draft": "draft text for Append / New Section / New File verdicts",
  "revision": {
    "reason": "why existing text is wrong or insufficient (Revise only)",
    "before": "text to replace (Revise only)",
    "after": "proposed replacement (Revise only)"
  }
}
```

## Exclusions

- Obvious principles already in rules
- Language/framework-specific knowledge (belongs in language-specific rules or skills)
- Code examples and commands (belong in skills)
````

#### Verdict reference

| Verdict | Meaning | Show the user |
|---------|---------|---------------|
| **Append** | Add to existing section | target + draft |
| **Revise** | Fix inaccurate or insufficient content | target + reason + before/after |
| **New Section** | New section in existing file | target + draft |
| **New File** | Create rule file | filename + full draft |
| **Already Covered** | Rules already cover it (maybe different wording) | one-line reason |
| **Too Specific** | Keep in skills | link to relevant skills |

#### Verdict quality bar

```
# Good
Append to rules/common/security.md §Input validation:
"Treat LLM output stored in memory or a knowledge base as untrusted—sanitize on write, validate on read."
Evidence: llm-memory-trust-boundary and llm-social-agent-anti-pattern both describe cumulative prompt-injection risk. Current security.md only covers human input validation; missing trust boundary for LLM output.

# Bad
Append to security.md: add LLM security principles
```

### Phase 3: User review and apply

#### Summary table

```
# Rule Creator Report

## Overview
Skills scanned: {N} | Rule files: {M} | Candidates: {K}

| # | Principle | Verdict | Target file/section | Confidence |
|---|-----------|---------|----------------------|------------|
| 1 | ... | Append | security.md §Input validation | high |
| 2 | ... | Revise | testing.md §TDD | medium |
| 3 | ... | New Section | coding-style.md | high |
| 4 | ... | Too Specific | — | — |

## Details
(per-candidate evidence, violation risk, draft text)
```

#### User actions

The user responds by number to:

* **Approve**: apply the draft as written
* **Modify**: edit the draft before applying
* **Skip**: do not apply this candidate

**Never modify rules automatically. Always require user approval.**

#### Save results

Store results in the skill directory (`results.json`):

* **Timestamp**: `date -u +%Y-%m-%dT%H:%M:%SZ` (UTC, second precision)
* **Candidate ID**: kebab-case from the principle (e.g. `llm-output-trust-boundary`)

```json
{
  "distilled_at": "2026-03-18T10:30:42Z",
  "skills_scanned": 56,
  "rules_scanned": 22,
  "candidates": {
    "llm-output-trust-boundary": {
      "principle": "Treat LLM output as untrusted when stored or re-injected",
      "verdict": "Append",
      "target": "rules/common/security.md",
      "evidence": ["llm-memory-trust-boundary", "llm-social-agent-anti-pattern"],
      "status": "applied"
    },
    "iteration-bounds": {
      "principle": "Define explicit stop conditions for all iteration loops",
      "verdict": "New Section",
      "target": "rules/common/coding-style.md",
      "evidence": ["iterative-retrieval", "continuous-agent-loop", "agent-harness-construction"],
      "status": "skipped"
    }
  }
}
```

## Example

### End-to-end run

```
$ /rule-creator

Rule Creator — Phase 1: Inventory
────────────────────────────────────────
Skills: scanned 56 files
Rules: 22 files (75 headings indexed)

Cross-reading analysis in progress...

[Subagent: batch 1 (agent/meta skills) ...]
[Subagent: batch 2 (coding/pattern skills) ...]
[Cross-batch merge: removed 2 duplicates, promoted 1 cross-batch candidate]

# Rule Creator Report

## Summary
Skills scanned: 56 | Rules: 22 files | Candidates: 4

| # | Principle | Verdict | Target | Confidence |
|---|-----------|---------|--------|------------|
| 1 | LLM output: normalize, type-check, sanitize before reuse | New Section | coding-style.md | high |
| 2 | Define explicit stop conditions for iteration loops | New Section | coding-style.md | high |
| 3 | Compress context at phase boundaries, not mid-task | Append | performance.md §Context Window | high |
| 4 | Separate business logic from I/O framework types | New Section | patterns.md | high |

## Details

### 1. LLM output validation
Verdict: New Section in coding-style.md
Evidence: parallel-subagent-batch-merge, llm-social-agent-anti-pattern, llm-memory-trust-boundary
Violation risk: format drift, type mismatch, or syntax errors in LLM output crash downstream handling
Draft:
  ## LLM output validation
  Before reusing LLM output, normalize, type-check, and sanitize...
  See skill: parallel-subagent-batch-merge, llm-memory-trust-boundary

[... details for candidates 2–4 ...]

Approve, modify, or skip each candidate by number:
> User: Approve 1, 3. Skip 2, 4.

✓ Applied: coding-style.md §LLM output validation
✓ Applied: performance.md §Context window management
✗ Skipped: iteration bounds
✗ Skipped: boundary type casting

Results saved to results.json
```

## Design principles

* **What, not how**: extract principles (rule scope). Keep code examples and commands in skills.
* **Link back**: draft text should include `See skill: [name]` so readers can find detailed how-to.
* **Deterministic collection, LLM judgment**: scripts ensure completeness; the LLM ensures contextual understanding.
* **Anti-abstraction guard**: three filters (2+ skill evidence, actionable behavior test, violation risk) keep overly abstract principles out of rules.
