"""Smoke tests for the shared agent core against the repo's seed data."""
from __future__ import annotations

import pytest

from agent_core import knowledge, tools, workflow


def test_search_finds_getting_started():
    results = knowledge.search("discovery")
    assert any(r["path"] == "methods/getting-started.md" for r in results)


def test_search_empty_query_raises():
    with pytest.raises(knowledge.KnowledgeError):
        knowledge.search("   ")


def test_read_returns_frontmatter():
    doc = knowledge.read("methods/getting-started.md")
    assert doc["frontmatter"]["id"] == "getting-started"
    assert "Getting started" in doc["content"]


def test_read_path_escape_raises():
    with pytest.raises(knowledge.KnowledgeError):
        knowledge.read("../agent/agent-name")


def test_workflow_list_includes_hello():
    ids = {w["id"] for w in workflow.list_workflows()}
    assert "hello" in ids


def test_workflow_run_hello_embeds_skill():
    result = workflow.run("hello", {"theme": "AI coaching"})
    step = result["steps"][0]
    assert step["type"] == "skill"
    assert step["ref"] == "research-ops"
    assert step["with"]["focus"] == "AI coaching"
    assert len(step["skill"]) > 0 and "skill not found" not in step["skill"]


def test_workflow_run_missing_input_raises():
    with pytest.raises(workflow.WorkflowError):
        workflow.run("hello", {})


def test_tool_registry_dispatch():
    out = tools.call("workflow_list", {})
    assert out["count"] >= 1
    assert len(tools.anthropic_schemas()) == 5
