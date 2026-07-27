# Step 2 — Summarize and confirm

Present a **research summary** in chat using the research-ops output format:

```text
Question type
- …

Evidence
- Sourced facts (with dates where time-sensitive)
- User-provided context

Inference
- …

Recommendation
- …
```

Then ask exactly:

> Are you satisfied with the research result? Say **yes** to confirm or give me feedback.

Do **not** write to `./knowledge/` until the user confirms with **yes** (or clear equivalent: "confirm", "looks good", "proceed to store").

This **yes** means “proceed to **store**” only. It does **not** mark the overall major task done and does **not** authorize samectx or retrospective (see `99-task-completion-gate.mdc` / `continuous-learning.mdc`).

If the user gives feedback instead of yes, proceed to the **revision-loop** step — not to storage.
