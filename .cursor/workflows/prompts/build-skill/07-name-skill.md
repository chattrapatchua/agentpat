# Step 7 — Skill folder name

Requires approved **Composed brief** from step `compose-skill-brief`.

## AskQuestion (required)

**Title:** `Build skill — name`

**Prompt:**

> Choose a **skill folder name** (kebab-case, 2–32 chars, letters/numbers/hyphens). This becomes `agent/define-skills/<name>/` and `.cursor/skills/<name>/`.

If `skill_hint` was provided in workflow inputs, suggest it as the default in the prompt text.

**Options:**

| `id` | Label |
| --- | --- |
| `answer-in-chat` | I'll type the skill name in my next message |

Wait for the next message; validate slug pattern `^[a-z0-9][a-z0-9-]{0,30}[a-z0-9]$|^[a-z0-9]{2}$`.

## Store

- **Skill slug:** (validated name)
