<div align="center">

# 🤖 Agents & Skills — Plugin Marketplace

**Private AI productivity plugins for JKH Group teams.**

Install once, use everywhere — **VS Code Copilot**, **Claude Code**, **Claude Desktop**, or **Copilot CLI**.

---

[What's Inside](#-whats-inside) · [Quick Start](#-quick-start) · [Private Distribution](#-private-distribution--security) · [Add to Any Project](#-add-to-any-project) · [How It Works](#-how-it-works) · [Create a Plugin](#-create-a-plugin) · [FAQ](#-faq)

</div>

---

## 📦 What's Inside

This repo is a **private plugin marketplace** — a catalog of installable plugins restricted to the JKH Group organization. Each plugin is self-contained and can be installed independently.

### Available Plugins

| Plugin | What It Includes | For Who |
|--------|-----------------|---------|
| **base-tools** | Deck skill — generates branded PowerPoint presentations (OCTAVE templates, shape-based diagrams) | All teams |
| **devops-team** | Time Logger agent — logs hours to Azure DevOps sprint boards. Handles multiple projects, detects board conventions, lets you undo changes. Includes Azure DevOps MCP server. | DevOps team |

---

## 🚀 Quick Start

Choose your platform. Each path gets you up and running independently.

### Option A: VS Code Copilot

> **Prerequisite:** `chat.plugins.enabled` must be `true` in your org's GitHub Copilot policy. Ask your admin if plugins aren't visible.

**Step 1 — Register the marketplace** (one time)

Open VS Code Settings (`Ctrl+,`) and add to `settings.json`:
```jsonc
// settings.json
"chat.plugins.marketplaces": [
    "hirushaud-jkh/agents-and-skills"
]
```

Or run **Chat: Install Plugin From Source** from the Command Palette and enter:
```
https://github.com/hirushaud-jkh/agents-and-skills
```

**Step 2 — Install plugins**

1. Open the **Extensions** sidebar (`Ctrl+Shift+X`)
2. Type `@agentPlugins` in the search field
3. Browse and click **Install** on the plugins you want

**Step 3 — Use it**

Open **Copilot Chat** → select **Time Logger** from the agent picker → say *"log my time"*

### Option B: Claude Code (CLI)

```bash
# 1. Add the marketplace (one time)
claude plugin marketplace add hirushaud-jkh/agents-and-skills

# 2. Install the plugins you need
claude plugin install base-tools@jkh-tools
claude plugin install devops-team@jkh-tools

# 3. When prompted, paste your Azure DevOps PAT
#    (stored securely in your system keychain)
```

Or use the interactive UI: run `/plugin` → **Discover** tab → select a plugin → choose scope.

### Option C: Claude Desktop

Claude Desktop supports MCP servers but not the full plugin system. You can use the Azure DevOps tools directly:

1. Open Claude Desktop → **Settings** → **Developer** → **Edit Config**
2. Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "JKGroupAA"],
      "env": {
        "AZURE_DEVOPS_EXT_PAT": "your-pat-here"
      }
    }
  }
}
```
3. Restart Claude Desktop — the Azure DevOps tools appear automatically
4. Say *"log 8 hours to my sprint tasks"* — Claude can use the work item tools directly

> **Note:** Claude Desktop gets the MCP tools (create/update work items, list sprints, etc.) but not the Time Logger agent persona. For the full agent experience, use VS Code or Claude Code.

### Option D: Copilot CLI

```bash
# Install from the marketplace
copilot plugin install devops-team@jkh-tools
```

---

### One-time setup (per tool)

<details>
<summary><b>Time Logger</b> — needs an Azure DevOps PAT</summary>

1. Go to [Azure DevOps → Personal Access Tokens](https://dev.azure.com/JKGroupAA/_usersSettings/tokens)
2. Create a new token with these scopes:
   - **Work Items** — Read & Write
   - **Project and Team** — Read
3. How the token is stored depends on your platform:
   - **Claude Code:** prompted interactively, stored in system keychain via `userConfig`
   - **VS Code:** set the `AZURE_DEVOPS_EXT_PAT` environment variable
   - **Claude Desktop:** hardcoded in `claude_desktop_config.json` (local file, not committed)

</details>

<details>
<summary><b>Deck</b> — needs python-pptx + templates</summary>

1. Install the Python dependency:
   ```bash
   pip install python-pptx
   ```
2. Place your `.pptx` template files in the `templates/` folder inside the skill directory
   - The skill auto-detects them at runtime
   - Templates are gitignored — each user provides their own

</details>

---

## 🔒 Private Distribution & Security

This marketplace is hosted in a **private GitHub repo** — only organization members with repo access can install plugins. No public exposure.

### How access control works

| Layer | Mechanism |
|-------|-----------|
| **Repo access** | GitHub repo permissions — only org members can clone/install |
| **Claude Code auth** | Uses your existing git credentials (`gh auth login`, SSH keys). For auto-updates, set `GITHUB_TOKEN` or `GH_TOKEN` env var |
| **VS Code auth** | Falls back to cloning via your GitHub credentials. Private repos work if you're authenticated with GitHub in VS Code |
| **Secrets (PAT)** | Stored in system keychain (Claude Code) or env var (VS Code). Never committed to repo |

### For administrators — lock down marketplace sources

Admins can restrict which marketplaces users are allowed to add using **managed settings**. This prevents users from installing plugins from untrusted sources.

**Claude Code** — create a managed settings file:
```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "hirushaud-jkh/agents-and-skills"
    }
  ],
  "extraKnownMarketplaces": {
    "jkh-tools": {
      "source": { "source": "github", "repo": "hirushaud-jkh/agents-and-skills" }
    }
  },
  "enabledPlugins": {
    "base-tools@jkh-tools": true,
    "devops-team@jkh-tools": true
  }
}
```

- `strictKnownMarketplaces` = allowlist. Empty array `[]` = complete lockdown (no marketplaces allowed). Only this repo = only this marketplace.
- `extraKnownMarketplaces` = auto-registers the marketplace so users don't need to run `add`.
- `enabledPlugins` = auto-enables specific plugins.

**VS Code** — use GitHub Copilot organization settings to control `chat.plugins.enabled` and `chat.plugins.marketplaces` at the org level.

### Enable auto-updates for private repos

For Claude Code background auto-updates to work with private repos, set the token in your shell profile:

```bash
# ~/.bashrc, ~/.zshrc, or PowerShell $PROFILE
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

> GitHub Actions in the same org automatically provides `GITHUB_TOKEN`.

---

## 🏢 Add to Any Project

Want your whole team to get the plugins automatically when they open a project? Add a settings file.

### For Claude Code + VS Code (shared format)

**`.claude/settings.json`** — works for both Claude Code and VS Code workspace plugin recommendations:
```json
{
  "extraKnownMarketplaces": {
    "jkh-tools": {
      "source": { "source": "github", "repo": "hirushaud-jkh/agents-and-skills" }
    }
  },
  "enabledPlugins": {
    "base-tools@jkh-tools": true,
    "devops-team@jkh-tools": true
  }
}
```

- **Claude Code:** when team members trust the project folder, they're prompted to install the marketplace and plugins.
- **VS Code:** plugins appear when filtering `@agentPlugins @recommended` in the Extensions view. A notification shows the first time a chat message is sent.

> A ready-to-copy version is in [`examples/project-settings.json`](examples/project-settings.json).

### Alternative: VS Code only

If your team only uses VS Code, you can also use `.github/copilot/settings.json` (same format).

---

## 🧩 How It Works

```
┌──────────────────────────────────────────────────────────────┐
│          You (VS Code, Claude Code, or Claude Desktop)       │
│                                                              │
│   "Log my time"               "Create a deck for Q3"        │
│        │                               │                     │
│        ▼                               ▼                     │
│   ┌────────────┐               ┌──────────────┐             │
│   │  Plugin:    │               │  Plugin:      │             │
│   │  devops-    │               │  base-tools   │             │
│   │  team       │               │               │             │
│   │  ┌────────┐ │               │  ┌──────────┐ │             │
│   │  │ Agent: │ │               │  │ Skill:   │ │             │
│   │  │ Time   │ │               │  │ Deck     │ │             │
│   │  │ Logger │ │               │  │ Generator│ │             │
│   │  └───┬────┘ │               │  └────┬─────┘ │             │
│   └──────┼──────┘               └───────┼───────┘             │
│          │                              │                     │
│          ▼                              ▼                     │
│   Azure DevOps                   PowerPoint file              │
│   (via MCP server)              (on your machine)             │
└──────────────────────────────────────────────────────────────┘
```

### Platform compatibility

The `.claude-plugin/` format is shared across all platforms. VS Code auto-detects it.

| Capability | VS Code Copilot | Claude Code | Claude Desktop | Copilot CLI |
|------------|:---------------:|:-----------:|:--------------:|:-----------:|
| Plugin install | `@agentPlugins` in Extensions | `/plugin install` | — (manual MCP) | `copilot plugin install` |
| Agents | ✅ | ✅ | ❌ | ✅ |
| Skills | ✅ | ✅ | ❌ | ✅ |
| MCP servers | ✅ (from plugin) | ✅ (from plugin) | ✅ (manual config) | ✅ |
| PAT auth | Env var | Keychain (`userConfig`) | Config file | Env var |
| Auto-update | Every 24h | On startup | — | On startup |
| Plugin dependencies | Manual install | Auto-resolved | — | Auto-resolved |

---

## 📁 Repo Structure

```
agents-and-skills/
│
├── .claude-plugin/
│   └── marketplace.json           ← Plugin catalog (lists all plugins)
│
├── plugins/
│   ├── base-tools/                ← Shared skills for all teams
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json        ← Plugin manifest
│   │   └── skills/
│   │       └── deck/
│   │           ├── SKILL.md       ← Deck generation instructions
│   │           ├── recipes.py     ← Python helpers (shapes, colors, layout)
│   │           └── templates/     ← Your .pptx files here (gitignored)
│   │
│   └── devops-team/               ← DevOps team tools
│       ├── .claude-plugin/
│       │   └── plugin.json        ← Plugin manifest (depends on base-tools)
│       ├── .mcp.json              ← Azure DevOps MCP server config
│       └── agents/
│           └── time-logger.md     ← Time Logger agent (self-contained)
│
├── examples/
│   └── project-settings.json     ← Copy into your project for auto-setup
│
├── CLAUDE.md                      ← Project context (read by both platforms)
└── README.md                      ← You are here
```

> **Key rule:** Each plugin is fully self-contained under `plugins/<name>/`. No cross-references between plugins. To change agent behavior, edit the agent file directly.

---

## ➕ Create a Plugin

Want to add tools for your team? Create a new plugin in 3 steps.

### 1. Create the plugin directory

```
plugins/your-team/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── your-agent.md          ← agent prompt (Markdown with YAML frontmatter)
└── skills/
    └── your-skill/
        └── SKILL.md           ← skill instructions
```

### 2. Write the plugin manifest

**`plugins/your-team/.claude-plugin/plugin.json`**
```json
{
  "name": "your-team",
  "description": "What your plugin does",
  "author": { "name": "JKH Group DevTools" },
  "keywords": ["your", "keywords"],
  "dependencies": ["base-tools"]
}
```

### 3. Register it in the marketplace

Add an entry to `.claude-plugin/marketplace.json`:
```json
{
  "name": "your-team",
  "source": "./plugins/your-team",
  "description": "What your plugin does",
  "category": "productivity",
  "keywords": ["your", "keywords"]
}
```

Then push to the repo. Users run `/plugin marketplace update jkh-tools` (Claude Code) or check for updates in VS Code to see the new plugin.

### Agent format

Agents are Markdown files with YAML frontmatter:
```yaml
---
name: your-agent
description: "Use when: <describe when the agent should be triggered>"
model: sonnet
tools: Tool1, Tool2, mcp__server__tool_name
---

# Your Agent

Write the behavioral prompt here in plain English.
The AI reads this and follows the instructions — no code required.
```

### Skill format

Skills live in a folder with a `SKILL.md`:
```yaml
---
name: your-skill
description: "What this skill does and when to use it"
---

# Your Skill

Instructions for the AI to follow when this skill is invoked.
```

### Adding an MCP server

If your plugin needs an MCP server, add `.mcp.json` at the plugin root:
```json
{
  "mcpServers": {
    "your-server": {
      "command": "npx",
      "args": ["-y", "@your-package/mcp"],
      "env": {
        "API_TOKEN": "${user_config.your_token}"
      }
    }
  }
}
```

And add `userConfig` to your `plugin.json` for secrets:
```json
{
  "userConfig": {
    "your_token": {
      "type": "string",
      "title": "Your API Token",
      "sensitive": true,
      "required": true
    }
  }
}
```

---

## ❓ FAQ

<details>
<summary><b>Do I need both VS Code and Claude Code?</b></summary>

No. Use whichever you have. Plugins work on each platform independently. Claude Desktop gives you MCP tools only (no agents/skills).
</details>

<details>
<summary><b>Do I need to clone this repo?</b></summary>

No. The plugin system installs directly from GitHub. You only clone if you're developing new plugins.
</details>

<details>
<summary><b>@agentPlugins shows nothing in VS Code</b></summary>

Three things to check:
1. **Marketplace registered?** Add `"chat.plugins.marketplaces": ["hirushaud-jkh/agents-and-skills"]` to your VS Code `settings.json`
2. **Plugins enabled?** `chat.plugins.enabled` must be `true` — this is an org-level setting, ask your GitHub Copilot admin
3. **Authenticated?** You need GitHub access to the private repo. Make sure you're signed in to GitHub in VS Code
</details>

<details>
<summary><b>How do I update to the latest version?</b></summary>

- **VS Code:** auto-checks every 24h, or run `Extensions: Check for Extension Updates` from Command Palette
- **Claude Code:** auto-updates on startup, or run `/plugin marketplace update jkh-tools`
- For private repos, ensure `GITHUB_TOKEN` is set for background auto-updates
</details>

<details>
<summary><b>The Time Logger agent isn't showing up</b></summary>

1. Make sure the `devops-team` plugin is installed and enabled
2. Reload VS Code (`Ctrl+Shift+P` → *Reload Window*)
3. In Claude Code, run `/reload-plugins` to refresh
4. Check plugin errors: VS Code Extensions sidebar → Agent Plugins view, or `/plugin` → Errors tab in Claude Code
</details>

<details>
<summary><b>Can I add agents without knowing how to code?</b></summary>

Yes. Agents and skills are Markdown files with plain English instructions. The AI reads your instructions and follows them. No programming required — just describe what the agent should do.
</details>

<details>
<summary><b>Is this marketplace public?</b></summary>

No. It's hosted in a private GitHub repo. Only organization members with repo access can install plugins. Admins can further restrict access using `strictKnownMarketplaces` in managed settings.
</details>

<details>
<summary><b>Are my tokens stored in the repo?</b></summary>

No. Tokens are either stored in your system keychain (Claude Code), passed via environment variables (VS Code), or in a local config file (Claude Desktop). Nothing sensitive is committed. The `.gitignore` blocks settings files and `.env` as a safety net.
</details>

<details>
<summary><b>Can different teams have their own plugins?</b></summary>

Yes — that's the whole idea. Each team creates a plugin under `plugins/<team-name>/` with their own agents, skills, and MCP servers. Teams can depend on `base-tools` for shared capabilities but are otherwise independent.
</details>

<details>
<summary><b>What if I only want some plugins, not all?</b></summary>

Install only what you need. Each plugin is independent:
```bash
# Just the shared skills
claude plugin install base-tools@jkh-tools

# Just the DevOps tools
claude plugin install devops-team@jkh-tools
```
In VS Code, pick individual plugins from the `@agentPlugins` view in Extensions.
</details>

<details>
<summary><b>Can I use this with Claude Desktop?</b></summary>

Partially. Claude Desktop supports MCP servers, so you get the Azure DevOps tools (create/update work items, list sprints, etc.). However, it doesn't support the plugin agent system, so you won't get the Time Logger agent persona — just the raw tools. See the [Claude Desktop setup](#option-c-claude-desktop) above.
</details>

---
