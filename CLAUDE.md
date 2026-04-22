# Project: agents-and-skills

Centralized repository for reusable AI agents and skills. Designed to work across both GitHub Copilot (VS Code) and Claude Code.

## Repo Structure

- `core/` — Platform-agnostic behavioral instructions (the source of truth for agent logic)
- `.claude/agents/` — Claude Code agent wrappers (also read by Copilot)
- `.github/agents/` — Copilot-enhanced agent wrappers (handoffs, model fallback arrays, `#tool:` refs)
- `.claude/skills/` — Shared skills (both Copilot and Claude Code discover this path)
- `.vscode/mcp.json` — MCP server config for VS Code / Copilot
- `.mcp.json` — MCP server config for Claude Code

## Conventions

- When editing agent behavior, edit the core prompt in `core/<agent>/prompt.md` — not the wrappers.
- Wrappers only contain frontmatter (tools, model, platform features) and a link to the core prompt.
- Tool names differ between platforms. The mapping table in each wrapper resolves this.
- MCP servers are configured in two files pointing to the same server — keep them in sync.

## Azure DevOps

- Organization: `JKGroupAA` (`https://dev.azure.com/JKGroupAA`)
- MCP package: `@azure-devops/mcp`
- Auth: Personal Access Token via environment variable `AZURE_DEVOPS_EXT_PAT`
