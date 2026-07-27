---
name: skill-lookup
description: >
  Search, retrieve, and install Agent Skills from the prompts.chat registry via MCP (search_skills,
  get_skill). Use when the user wants to find skills, browse catalogs, install a skill, extend agent
  capabilities, or asks "is there a skill for X". Search before authoring a new skill from scratch.
  In Work Agent repo install to .cursor/skills/{slug}/; elsewhere use ~/.cursor/skills/{slug}/ (not ~/.claude/skills).
license: MIT
---

# Skill Lookup

## Workflow

1. Search with `search_skills` for the user's request
2. Present title, description, author, files, category/tags, and link
3. On pick, call `get_skill` for full file contents
4. Install under `.cursor/skills/{slug}/` when working in the Work Agent repo; otherwise `~/.cursor/skills/{slug}/`. Optional mirror: `work_agent_rules_skills/Skills/`
5. Confirm install; summarize what the skill does and when it should trigger

## Example

```
search_skills({"query": "code review", "limit": 5, "category": "coding"})
get_skill({"id": "abc123"})
```

## MCP tools

- `search_skills` — keyword search; optional `limit`, `category`, `tag`
- `get_skill` — metadata + all files by `id`

## Install layout

**Work Agent project (preferred when in this repo):**

```
.cursor/skills/{slug}/SKILL.md
.cursor/skills/{slug}/...  # references, scripts, assets
```

**Global (other projects):**

```
~/.cursor/skills/{slug}/SKILL.md
~/.cursor/skills/{slug}/...
```

After install, read back `SKILL.md` frontmatter (`name`, `description`) to verify triggering text is intact.

## Guidelines

- Search the registry before recommending a custom skill
- Show readable results with file counts
- Explain activation (description field drives when agents load the skill)
- Do not install into legacy `~/.claude/skills` unless the user explicitly uses Claude Code only without Cursor sync
