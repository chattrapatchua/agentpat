# Step 10 — Deploy skill to IDE

Requires **`agent/define-skills/<skill-slug>/SKILL.md`**.

## Deploy

1. Mirror draft into production:
   ```bash
   bash scripts/deploy-ide-assets.sh
   ```
2. Verify:
   ```bash
   bash scripts/verify-ide-setup.sh --strict
   ```
3. Confirm: `.cursor/skills/<skill-slug>/SKILL.md` (or `$IDE_DIR/skills/` per `agent/ide-target`).

Tell the user draft vs runtime paths. Continue to **task-completion-gate**.
