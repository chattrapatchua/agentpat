---
name: research-ops
description: Evidence-first ECC current-state research workflow. Use when the user wants up-to-date facts, comparisons, enrichment, or recommendations based on current public evidence and provided local context.
origin: ECC
---

# Research Ops

Use this when the user asks to research current information, compare options, enrich people or companies, or turn a repeated query into a monitorable workflow.

This is an operational wrapper around the repo research stack. It is not a replacement for `deep-research`, `exa-search`, or `market-research`; it tells you when and how to combine them.

## Skill stack

Bring these ECC-native skills into the workflow when relevant:

* `exa-search`: for fast discovery of current web information
* `deep-research`: for multi-source synthesis with citations
* `market-research`: when the end result should be a recommendation or ranked decision
* `lead-intelligence`: when the task targets people/companies rather than general research
* `knowledge-ops`: when results need to persist for later context

## When to use

* The user mentions "research", "look up", "compare", "who should I contact", or "what's the latest"
* The answer depends on current public information
* The user has already provided evidence and wants it folded into a new recommendation
* The task may be repetitive and should become monitoring rather than a one-off query

## Guardrails

* Do not answer current questions from stale memory when a fresh search is cheap
* Distinguish:
  * Sourced facts
  * User-provided evidence
  * Inference
  * Recommendation
* If the answer already exists in local code or docs, do not start a heavy research flow

## Workflow

### 1. Start from what the user already provided

Normalize any provided material into:

* Facts already supported by evidence
* Things that need verification
* Open questions

If the user has already built part of a model, do not re-analyze from scratch.

### 2. Classify the request

Before searching, pick the right path:

* Quick factual answer
* Comparison or decision memo
* Lead / enrichment handling
* Repeat-monitoring candidate

### 3. Prefer the lightest effective evidence path

* Use `exa-search` for fast discovery
* Escalate to `deep-research` when synthesis or multi-source coverage is needed
* Use `market-research` when the result should be framed as a recommendation
* Hand off to `lead-intelligence` when the real need is target ranking or warm-path discovery

### 4. Report with clear evidence boundaries

For important claims, state whether they are:

* Sourced facts
* User-provided context
* Inference
* Recommendation

Time-sensitive answers should include concrete dates.

### 5. Decide whether the task should stay manual

If the user is likely to ask the same research question again, say so explicitly and suggest a monitoring or workflow layer instead of forever repeating the same manual search.

## Output format

```text
Question type
- Factual / Comparative / Enrichment / Monitoring

Evidence
- Sourced facts
- User-provided context

Inference
- Conclusions drawn from the evidence

Recommendation
- Answer or next actions
- Whether this should become a monitor
```

## Common pitfalls

* Do not mix inference into sourced facts without labeling
* Do not ignore user-provided evidence
* Do not use a heavy research path for questions local repo context can answer
* Do not give time-sensitive answers without dates

## Validation

* Important claims are labeled by evidence type
* Time-sensitive outputs include dates
* Final recommendations match the research mode actually used
