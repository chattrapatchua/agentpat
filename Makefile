.PHONY: help install build test dev up down call-agent onboard-agent rename-agent call-agent-agentpat onboard-agent-agentpat

.DEFAULT_GOAL := help

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

call-agent: ## Open Cursor (slug from agent/agent-name)
	@bash scripts/call-agent.sh

call-agent-agentpat: ## Same as call-agent when slug is agentpat
	@bash scripts/call-agent.sh

onboard-agent: ## First-time clone (optional), install, build, open Cursor
	@bash scripts/onboard-agent.sh

onboard-agent-agentpat: ## Same as onboard-agent
	@bash scripts/onboard-agent.sh

rename-agent: ## Rename agent: make rename-agent NEW=alex
	@test -n "$(NEW)" || (echo "Usage: make rename-agent NEW=<slug>"; exit 1)
	@bash scripts/rename-agent.sh "$(NEW)"

install: ## Install npm dependencies (monorepo)
	npm install

build: ## Build agent-core and mcp-server
	npm run build

test: ## Run agent-core tests
	npm run test

dev: ## Same as call-agent
	@bash scripts/call-agent.sh

up: ## Alias for build (MCP is started by Cursor, not background here)
	$(MAKE) build

down: ## No-op for MVP (no background services)
	@true
