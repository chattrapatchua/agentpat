# S-Situation
- I am doing Product Discovery and Strategy for **new innovations** (ideas not yet tied to a fixed market/product).
- I have **no chosen business domain** yet (industry, market, or product category). I will specify the domain after the innovation direction is clear; until then, treat domain as unset.
- I need to run market research, generate customer or user insights, discover business opportunities, and define product strategy using techniques such as personas, elevator pitch, business requirements (BRD), and product prototype narratives or demos.
- I may use AI (including agents) as part of these workflows; methods and artifacts should work across domains once I provide context.
- I need my personalized AI Agent as my co-pilot for discovery and strategy work.
- The agent runs in **Cursor Agent mode** (rules, skills, **work-agent** MCP) and will later support a **web chat UI** sharing the same core (see `agent/architecture.md`).

# T-Task
Help me create and train my agent by
- providing prompts
- improve skills
- define rules
- define workflows
- manage knowledges in `./knowledge`
- wire **MCP** (`packages/mcp-server`, `.cursor/mcp.json`) for knowledge and workflow tools
- improve the way how the agent interact with the user