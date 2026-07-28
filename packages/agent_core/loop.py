"""Agent loop for the web chat. The MCP path uses Cursor's own model, so this is web-only.

Detects an API key (Anthropic preferred, else OpenAI), runs a tool-use loop over the
shared registry, and yields events for SSE. MVP streams per-step events
(tool_call / tool_result / text / done), not individual tokens.
"""
from __future__ import annotations

import json
import os

from . import config, tools

SYSTEM_PROMPT = (
    "You are the Work Agent, a product-discovery and strategy co-pilot. You help with market "
    "research, personas, elevator pitches, BRDs, and opportunity discovery. Ground answers in the "
    "repo knowledge base: call knowledge_search / knowledge_read before answering factual questions, "
    "cite the knowledge path you used, and use knowledge_write to persist durable insights. Use "
    "workflow_list / workflow_run for named procedures. Be concise and concrete."
)


def provider() -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return "none"


def _summ(result: dict) -> str:
    s = json.dumps(result, default=str)
    return s if len(s) <= 600 else s[:600] + "…"


def _exec_tool(name: str, args: dict) -> tuple[dict, bool]:
    try:
        return tools.call(name, args), False
    except Exception as exc:  # surface as a tool error; keep the loop alive
        return {"error": type(exc).__name__, "message": str(exc)}, True


def run_turn(messages: list[dict]):
    """Yield event dicts for one user turn. `messages` is the running chat history."""
    p = provider()
    if p == "anthropic":
        yield from _run_anthropic(messages)
    elif p == "openai":
        yield from _run_openai(messages)
    else:
        yield {
            "type": "error",
            "message": "No model API key set. Add ANTHROPIC_API_KEY or OPENAI_API_KEY to .env.",
        }
        yield {"type": "done"}


def _run_anthropic(messages: list[dict]):
    import anthropic

    client = anthropic.Anthropic()
    convo = list(messages)
    schemas = tools.anthropic_schemas()

    for _ in range(config.MAX_STEPS):
        resp = client.messages.create(
            model=config.ANTHROPIC_MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=schemas,
            messages=convo,
        )
        assistant, texts, tool_uses = [], [], []
        for block in resp.content:
            if block.type == "text":
                texts.append(block.text)
                assistant.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                tool_uses.append(block)
                assistant.append(
                    {"type": "tool_use", "id": block.id, "name": block.name, "input": block.input}
                )
        convo.append({"role": "assistant", "content": assistant})
        if texts:
            yield {"type": "text", "text": "\n".join(texts)}
        if resp.stop_reason != "tool_use" or not tool_uses:
            break

        results = []
        for tu in tool_uses:
            yield {"type": "tool_call", "name": tu.name, "input": tu.input}
            result, is_err = _exec_tool(tu.name, tu.input)
            yield {"type": "tool_result", "name": tu.name, "error": is_err, "result": _summ(result)}
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": json.dumps(result, default=str),
                    "is_error": is_err,
                }
            )
        convo.append({"role": "user", "content": results})

    yield {"type": "history", "messages": convo}
    yield {"type": "done"}


def _run_openai(messages: list[dict]):
    from openai import OpenAI

    client = OpenAI()
    convo = [{"role": "system", "content": SYSTEM_PROMPT}] + list(messages)
    schemas = tools.openai_schemas()

    for _ in range(config.MAX_STEPS):
        resp = client.chat.completions.create(
            model=config.OPENAI_MODEL, messages=convo, tools=schemas
        )
        msg = resp.choices[0].message
        convo.append(msg.model_dump(exclude_none=True))
        if msg.content:
            yield {"type": "text", "text": msg.content}
        if not msg.tool_calls:
            break

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            yield {"type": "tool_call", "name": tc.function.name, "input": args}
            result, is_err = _exec_tool(tc.function.name, args)
            yield {"type": "tool_result", "name": tc.function.name, "error": is_err, "result": _summ(result)}
            convo.append(
                {"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result, default=str)}
            )

    yield {"type": "history", "messages": convo[1:]}  # drop the system message
    yield {"type": "done"}
