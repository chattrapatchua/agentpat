# Step 6 — Compose skill prompt

Requires completed **Q1–Q5** in the Skill build brief.

## Generate the core prompt block

Produce this structure for the body of the new skill (and show the user for confirmation):

```markdown
# Situation
<!-- Summarize Q1 in 2–4 sentences, first-person → third-person situation -->

# Role
<!-- Summarize Q2 -->

# Knowledge
<!-- Summarize Q3: KB paths, search strategy -->

# Task
<!-- Default core task PLUS Q4 behavior -->

Default task (always include, adapt wording only if user contradicts):

Based on the situation, play the specified role. Search and retrieve the knowledge base for required knowledge (`knowledge_search`, `knowledge_read` via work-agent MCP, or read `./knowledge/`). If knowledge is missing or stale, use the **learn-knowledge** workflow (or `research-ops`) to add it before answering. Then execute the specific behaviors described above.

# Rule
<!-- Summarize Q5 as bullet rules -->
```

## Confirm

Use **AskQuestion**:

**Prompt:** `Does this skill brief look correct before we name the skill and run skill-creator?`

| `id` | Label |
| --- | --- |
| `approve-brief` | Approve — continue to name skill |
| `revise-brief` | Revise — I'll specify changes in chat |

If **revise-brief**, update the block from user feedback and ask again.

## Store

- **Composed brief:** (final markdown block)
