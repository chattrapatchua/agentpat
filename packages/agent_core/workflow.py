"""Workflow engine: list and run declarative YAML workflows from .cursor/workflows.

MVP execution (see agent/mvp-cursor.md):
  - `skill`  steps embed .cursor/skills/{ref}/SKILL.md so the calling model runs the flow.
  - `prompt` steps return the referenced template text as instructions.
  - `tool`   steps return the tool name + templated args as an instruction (not run here).

Side-effecting, model-driven execution stays with the caller (Cursor or the web loop),
not baked into this engine.
"""
from __future__ import annotations

import datetime as _dt

import yaml

from . import config


class WorkflowError(Exception):
    """Workflow not found or missing a required input."""


def _load_all() -> list[dict]:
    base = config.WORKFLOWS_DIR
    if not base.exists():
        return []
    out: list[dict] = []
    for path in sorted(base.rglob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(data, dict) and data.get("id"):
            data["_path"] = path.relative_to(config.ROOT).as_posix()
            out.append(data)
    return out


def list_workflows() -> list[dict]:
    """Enumerate workflows with their inputs and descriptions."""
    return [
        {
            "id": wf.get("id"),
            "title": wf.get("title", wf.get("id")),
            "description": (wf.get("description") or "").strip(),
            "interactive": bool(wf.get("interactive", False)),
            "inputs": wf.get("inputs", []),
            "path": wf.get("_path"),
        }
        for wf in _load_all()
    ]


def _get(wf_id: str) -> dict:
    for wf in _load_all():
        if wf.get("id") == wf_id:
            return wf
    raise WorkflowError(f"workflow not found: {wf_id}")


def _substitute(value, inputs: dict):
    if not isinstance(value, str):
        return value
    out = value.replace("{{date}}", _dt.date.today().isoformat())
    for key, val in inputs.items():
        out = out.replace("{{inputs.%s}}" % key, str(val))
    return out


def _load_skill(ref: str) -> str:
    p = config.SKILLS_DIR / ref / "SKILL.md"
    return p.read_text(encoding="utf-8") if p.exists() else f"[skill not found: {ref}]"


def _load_template(rel: str) -> str:
    p = config.WORKFLOWS_DIR / rel
    return p.read_text(encoding="utf-8") if p.exists() else f"[template not found: {rel}]"


def run(wf_id: str, inputs: dict | None = None, session_id: str | None = None) -> dict:
    """Load a workflow, validate inputs, and resolve each step to instructions/content."""
    wf = _get(wf_id)
    inputs = inputs or {}

    missing = [
        i["name"] for i in wf.get("inputs", []) if i.get("required") and i["name"] not in inputs
    ]
    if missing:
        raise WorkflowError(f"missing required inputs: {', '.join(missing)}")

    steps: list[dict] = []
    for step in wf.get("steps", []):
        stype = step.get("type")
        entry: dict = {"id": step.get("id"), "type": stype}
        if stype == "skill":
            entry["ref"] = step.get("ref")
            entry["with"] = {k: _substitute(v, inputs) for k, v in (step.get("with") or {}).items()}
            entry["skill"] = _load_skill(step.get("ref", ""))
        elif stype == "prompt":
            entry["template_ref"] = step.get("template")
            entry["instructions"] = _substitute(_load_template(step.get("template", "")), inputs)
        elif stype == "tool":
            entry["tool"] = step.get("tool")
            entry["with"] = {k: _substitute(v, inputs) for k, v in (step.get("with") or {}).items()}
            entry["note"] = "Execute this tool with the given args."
        else:
            entry["note"] = f"unsupported step type: {stype}"
        steps.append(entry)

    return {
        "id": wf_id,
        "title": wf.get("title", wf_id),
        "session_id": session_id,
        "interactive": bool(wf.get("interactive", False)),
        "steps": steps,
        "status": "completed",
    }
