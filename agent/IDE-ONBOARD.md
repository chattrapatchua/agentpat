# IDE onboarding

On **`./onboard-agent-dan`**:

1. **Choose IDE** — Claude, Codex, Cursor, or Other (custom folder name).
2. **Write** [`ide-target`](ide-target) — `IDE`, `IDE_DIR` (e.g. `.cursor`, `.claude`).
3. **Ensure canonical** — `ensure-ide-canonical.sh` (git restore `.cursor/`, overlay `agent/define-*`, `ensure-mcp-config.sh`).
4. **Deploy** — full mirror of `.cursor/{rules,skills,workflows}` → **`$IDE_DIR/`** (your IDE’s folder).
5. **Verify** — `verify-ide-setup.sh --strict` diffs `$IDE_DIR` against `.cursor` for non-Cursor targets.

| Choice | Folder | What loads where |
| --- | --- | --- |
| Cursor | `.cursor/` | Rules, skills, workflows, **`mcp.json`** (work-agent) |
| Claude | `.claude/` | Same asset tree; MCP via `WORK_AGENT_IDE_DIR=.claude` (see README-ide.md) |
| Codex | `.codex/` | Same |
| Other `foo` | `.foo/` | Sanitized name; add to `.gitignore` if new |

**Canonical source:** `.cursor/` in git. Other folders are **generated copies** (gitignored). Onboard always refreshes `.cursor` first, then copies to `$IDE_DIR`.

**MCP**

| IDE | Config |
| --- | --- |
| Cursor | `.cursor/mcp.json` → `scripts/run-work-agent-mcp.sh` |
| Other | `WORK_AGENT_IDE_DIR=$IDE_DIR bash scripts/run-work-agent-mcp.sh` (workflows/skills paths follow `ide-target`) |

**Routine:** `./call-agent-dan` re-runs deploy if `$IDE_DIR` is out of sync with `.cursor`.

**Test all targets:** `bash scripts/test-ide-deploy.sh`

**Continuous-learning (Cursor):** Enable **Hooks** in Cursor settings; project `.cursor/hooks.json` nudges task-done **AskQuestion** after substantive edits. Rules alone do not auto-run samectx — see `continuous-learning.mdc`.

**Re-sync after pull:**

```bash
bash scripts/deploy-ide-assets.sh
bash scripts/verify-ide-setup.sh --strict
```

## Scripts (IDE-neutral names)

| Script | Purpose |
| --- | --- |
| `select-ide.sh` | Prompt or flags → `agent/ide-target` |
| `ensure-ide-canonical.sh` | Git restore + draft overlay → `.cursor/` |
| `ensure-mcp-config.sh` | `.cursor/mcp.json`, `MCP.md` (bootstrap: `agent/ide-bootstrap/mcp/`) |
| `deploy-ide-assets.sh` | Mirror `.cursor/` → `$IDE_DIR/` |
| `verify-ide-setup.sh` | Layout checks; `--strict` for full parity |
| `read-ide-target.sh` | Source for `IDE`, `IDE_DIR`, `IDE_LABEL` |
| `test-ide-deploy.sh` | Smoke test Claude / Codex / Other deploy |
| `run-work-agent-mcp.sh` | MCP stdio entry (reads `ide-target` for workflow paths) |

