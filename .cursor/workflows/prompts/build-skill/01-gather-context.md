# Step 1 — Context / background

Collect **Question 1** before continuing.

## AskQuestion (required)

Use **AskQuestion** with exactly one question:

**Title:** `Build skill — context`

**Prompt:**

> What context or background should this skill assume? Write in **first person** (as the user).
>
> Example: *I'm doing product discovery for a new Agentic Consumer-insight Portal for an infant formula marketing team.*

**Options:**

| `id` | Label |
| --- | --- |
| `answer-in-chat` | I'll answer in my next message |

After the user selects **I'll answer in my next message**, wait for their **next chat message** and treat it as the answer. Do not advance until you have a concrete context paragraph.

## Store

Keep a running **Skill build brief** in the thread (you will reuse it in step `compose-skill-brief`):

- **Q1 Context:** (user answer)
