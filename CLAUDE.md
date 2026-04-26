# Project: agents-and-skills

Plugin marketplace for JKH Group AI productivity tools. Cross-platform — works on GitHub Copilot (VS Code), Claude Code, Claude Desktop (MCP only), and Copilot CLI. Private repo — org members only.

## Architecture

This repo is a **plugin marketplace** — a catalog of installable plugins distributed via the `.claude-plugin/` format (shared between VS Code, Copilot CLI, and Claude Code).

## Repo Structure

```
.claude-plugin/marketplace.json    ← Marketplace catalog (lists all plugins)
plugins/
  base-tools/                      ← Shared plugin — skills used by all teams
    .claude-plugin/plugin.json
    skills/deck/                   ← PowerPoint generation (OCTAVE branding)
  devops-team/                     ← DevOps team — Azure DevOps integration
    .claude-plugin/plugin.json
    agents/time-logger.md          ← Time tracking agent
    .mcp.json                      ← Azure DevOps MCP server
```

## How to Install

**VS Code Copilot (GUI):**
1. Add to VS Code `settings.json`: `"chat.plugins.marketplaces": ["hirushaud-jkh/agents-and-skills"]`
2. Extensions sidebar → `@agentPlugins` → Install plugins
3. Requires `chat.plugins.enabled: true` (org-level setting)

**Claude Code (CLI):**
```bash
claude plugin marketplace add hirushaud-jkh/agents-and-skills
claude plugin install devops-team@jkh-tools
```

**Claude Desktop:** Add MCP server manually to `claude_desktop_config.json` (agents/skills not supported, MCP tools only).

**Project auto-setup:** Add to any project's `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "jkh-tools": {
      "source": { "source": "github", "repo": "hirushaud-jkh/agents-and-skills" }
    }
  },
  "enabledPlugins": { "devops-team@jkh-tools": true }
}
```

## Conventions

- Each plugin is self-contained under `plugins/<name>/` — no cross-references between plugins.
- Agent prompts live directly in the plugin's `agents/` directory (not in a separate `core/` folder).
- MCP servers are configured per-plugin in `.mcp.json` at the plugin root.
- No `version` field in `plugin.json` — every git commit is a new version (SHA-based). Switch to semver for stable releases.

## Azure DevOps

- Organization: `JKGroupAA` (`https://dev.azure.com/JKGroupAA`)
- MCP package: `@azure-devops/mcp`
- Auth: PAT prompted at plugin install (Claude Code) or via `AZURE_DEVOPS_EXT_PAT` env var (VS Code)
