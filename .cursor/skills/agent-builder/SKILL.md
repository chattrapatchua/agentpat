---
name: agent-builder
description: >
  Design and build AI agents (tool loops, capabilities, subagents, skills). Use when the user says
  create/build an agent or assistant, agent architecture, tool use, orchestration, multi-step autonomy,
  Claude Code/Cursor-style harnesses, or domain bots (support, research, ops, creative). Start minimal
  (3–5 tools); use scripts/init_agent.py to scaffold. Prefer real APIs and env-based secrets — no mock
  "fake agent" demos unless the user allows it.
---

# Agent Builder

Build AI agents for any domain — customer service, research, operations, creative work, or specialized business processes.

## Woodensword defaults

- **Real integrations**: wire tools to real APIs, DBs, or approved sandboxes (`persistent-proactive-developer` rule).
- **One capability at a time**: deliver one agent milestone to DoD before expanding (`incremental-delivery`).
- **New agent repo**: add root **Makefile** with `dev` / `up` / `down` when scaffolding a standalone project (`makefile` rule).
- **Logic worth keeping**: unit-test pure tool handlers and parsers (**tdd** + **common-test-strategy**).

## Work Agent repo (this project)

When building **this** agent, follow [`agent/architecture.md`](../../architecture.md):

- Cursor: rules/skills in `.cursor/` + **work-agent** MCP (`packages/mcp-server`, `.cursor/mcp.json`)
- Knowledge: `./knowledge/` via MCP `knowledge_*` tools
- Workflows: production YAML in `.cursor/workflows/` via `workflow_list` / `workflow_run`
- Draft authoring: `agent/define-*` → promote to `.cursor/`

## The core philosophy

> **The model already knows how to be an agent. Your job is to get out of the way.**

An agent is not complex engineering. It's a simple loop that invites the model to act:

```
LOOP:
  Model sees: context + available capabilities
  Model decides: act or respond
  If act: execute capability, add result, continue
  If respond: return to user
```

**That's it.** The magic isn't in the code — it's in the model. Your code provides the opportunity and guardrails.

## The three elements

### 1. Capabilities (what can it do?)

Atomic actions: search, read, create, send, query, modify.

**Design principle**: Start with 3–5 capabilities. Add more only when the agent consistently fails because a capability is missing.

### 2. Knowledge (what does it know?)

Domain expertise injected on demand: policies, workflows, best practices, schemas.

**Design principle**: Make knowledge available, not mandatory. Load when relevant, not upfront.

### 3. Context (what has happened?)

Conversation history — the thread connecting actions into coherent behavior.

**Design principle**: Context is precious. Isolate noisy subtasks. Truncate verbose outputs. Protect clarity.

## Before building

- **Purpose**: What should this agent accomplish?
- **Domain**: Customer service, research, operations, creative, etc.
- **Capabilities**: What 3–5 actions are essential?
- **Knowledge**: What expertise should load on demand?
- **Trust**: What decisions can you delegate to the model?

Trust the model. Avoid pre-specifying every workflow. Give capabilities and clear constraints; let it reason.

## Scaffold a new project

When the user wants a runnable starter (not just advice):

```bash
python scripts/init_agent.py <agent-name> [--level 0-4] [--path <output-dir>]
```

| Level | Typical use |
| --- | --- |
| 0 | Minimal — bash-only tool surface |
| 1 | Default — small tool set |
| 2 | Adds progress / todo tracking |
| 3+ | Subagents, richer patterns — only when needed |

Then customize tools in the generated project; read **`references/minimal-agent.py`** and **`references/tool-templates.py`** when implementing, not before scoping.

## Progressive complexity

| Level | What to add | When |
| --- | --- | --- |
| Basic | 3–5 capabilities | Always start here |
| Planning | Progress tracking | Multi-step tasks lose coherence |
| Subagents | Isolated child agents | Exploration pollutes context |
| Skills | On-demand knowledge | Domain expertise needed |

Most agents never need to go beyond Level 2.

## Anti-patterns

| Pattern | Problem | Fix |
| --- | --- | --- |
| Over-engineering | Complexity before need | Start simple |
| Too many capabilities | Model confusion | 3–5 to start |
| Rigid workflows | Can't adapt | Capabilities + constraints |
| Front-loaded knowledge | Context bloat | Load on demand |
| Mock-only tools | False "done" | Real or sandbox APIs |

## References (load when implementing)

| File | When |
| --- | --- |
| `references/agent-philosophy.md` | Theory, trust boundaries, design rationale |
| `references/minimal-agent.py` | Complete minimal loop |
| `references/tool-templates.py` | Capability definitions |
| `references/subagent-pattern.py` | Context isolation |
| `scripts/init_agent.py` | New project scaffold |

## Mindset shift

**From**: "How do I make the system do X?"  
**To**: "How do I enable the model to do X?"

**From**: "What's the workflow for this task?"  
**To**: "What capabilities would help accomplish this?"

Agent code should stay boring: simple loops, clear capabilities, clean context.
