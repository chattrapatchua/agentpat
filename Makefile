.PHONY: help install build test dev up down web mcp call-agent onboard-agent rename-agent call-agent-agentpat onboard-agent-agentpat

.DEFAULT_GOAL := help

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-22s %s\n", $$1, $$2}'

install: ## Create .venv and install (editable) with dev deps
	@bash scripts/onboard-agent.sh --no-open

build: ## No build step for Python (kept for parity)
	@echo "Python — nothing to build. Run 'make install' once, then 'make mcp' or 'make web'."

test: ## Run the agent-core test suite
	@bash scripts/run-tests.sh

mcp: ## Run the work-agent MCP server on stdio (normally started by Cursor)
	@bash scripts/run-work-agent-mcp.sh

web: ## Run the web chat UI + API (http://127.0.0.1:8765)
	@bash scripts/run-web.sh

call-agent: ## Ensure env, open Cursor (slug from agent/agent-name)
	@bash scripts/call-agent.sh

call-agent-agentpat: ## Same as call-agent when slug is agentpat
	@bash scripts/call-agent.sh

onboard-agent: ## First-time setup: venv, install, open Cursor
	@bash scripts/onboard-agent.sh

onboard-agent-agentpat: ## Same as onboard-agent
	@bash scripts/onboard-agent.sh

rename-agent: ## Rename agent: make rename-agent NEW=alex
	@test -n "$(NEW)" || (echo "Usage: make rename-agent NEW=<slug>"; exit 1)
	@bash scripts/rename-agent.sh "$(NEW)"

dev: ## Same as call-agent
	@bash scripts/call-agent.sh

up: ## Alias for install
	$(MAKE) install

down: ## No-op (no background services)
	@true
