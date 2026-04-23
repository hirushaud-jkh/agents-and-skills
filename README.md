<div align="center">

# 🤖 Agents & Skills

**A shared library of AI agents and skills for your team.**

Works with both **GitHub Copilot** (VS Code) and **Claude Code** — write once, use everywhere.

---

[What's Inside](#-whats-inside) · [Quick Start](#-quick-start) · [How It Works](#-how-it-works) · [Add Your Own](#-add-your-own) · [FAQ](#-faq)

</div>

---

## 📦 What's Inside

### Agents — AI assistants that do work for you

| Agent | What It Does | How to Use |
|-------|-------------|------------|
| **Time Logger** | Logs your hours to Azure DevOps sprint boards. Detects project conventions automatically, handles multiple projects in one session, and lets you undo changes. | Open chat → select **Time Logger** → say *"log time"* |

### Skills — Reusable capabilities you can invoke anytime

| Skill | What It Does | How to Use |
|-------|-------------|------------|
| **Deck** | Generates branded PowerPoint presentations using your company templates. Supports creating, editing, and referencing existing decks. | Type `/deck` in chat → follow the prompts |

---

## 🚀 Quick Start

### Step 1: Get the repo

```bash
git clone https://github.com/hirushaud-jkh/agents-and-skills.git
cd agents-and-skills
```

### Step 2: Run the installer

Works on **Windows, Mac, and Linux** — same command:

```bash
python setup.py
```

The installer asks two simple questions:

```
  Where do you want to install?

  [1] Global  - works in every VS Code workspace  (recommended)
  [2] Project - works in one specific folder
  [3] Both    - global + a specific project

  What do you want to install?

  [1] Everything         - agents, skills, and MCP config  (recommended)
  [2] Copilot agents     - just VS Code / GitHub Copilot
  [3] Claude agents      - just Claude Code
  [4] Skills             - just skills (Deck, etc.)
  [5] MCP config         - just Azure DevOps server setup
```

> **Most people:** Pick `1` then `1`. Done in 10 seconds.

### Step 3: Reload VS Code

`Ctrl+Shift+P` → *Reload Window* → open Copilot Chat → agents are ready.

---

### Quick install (skip the menu)

```bash
python setup.py --global                        # Everything, globally
python setup.py --project /path/to/my-project   # Everything, into one project
python setup.py --global --copilot              # Only Copilot agents, globally
```

<details>
<summary><b>Update / Uninstall</b></summary>

```bash
# Update: pull latest and re-run
git pull && python setup.py --global

# Uninstall: removes everything cleanly
python setup.py --uninstall
```

</details>

---

### One-time setup (per tool)

<details>
<summary><b>Time Logger</b> — needs Azure DevOps access</summary>

1. Get a **Personal Access Token** from [Azure DevOps](https://dev.azure.com/JKGroupAA/_usersSettings/tokens)
   - Scopes needed: **Work Items** (Read & Write), **Project and Team** (Read)
2. The installer configures this automatically — VS Code will prompt for the token securely on first use

</details>

<details>
<summary><b>Deck</b> — needs PowerPoint templates</summary>

1. After running the installer, copy your `.pptx` template files to:
   - **Windows:** `%USERPROFILE%\.claude\skills\deck\templates\`
   - **Mac/Linux:** `~/.claude/skills/deck/templates/`
2. The skill auto-detects any `.pptx` files placed there
3. Requires `python-pptx` — install with: `pip install python-pptx`

</details>

---

## 🧩 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    You (in VS Code or CLI)                   │
│                                                             │
│   "Log my time"              "/deck quarterly report"       │
│        │                              │                     │
│        ▼                              ▼                     │
│   ┌──────────┐                 ┌────────────┐              │
│   │  Agent:   │                 │   Skill:   │              │
│   │  Time     │                 │   Deck     │              │
│   │  Logger   │                 │   Generator│              │
│   └────┬─────┘                 └─────┬──────┘              │
│        │                              │                     │
│        ▼                              ▼                     │
│   Azure DevOps                  PowerPoint file             │
│   (work items created)          (on your machine)           │
└─────────────────────────────────────────────────────────────┘
```

### Platform compatibility

Both GitHub Copilot and Claude Code read from the **same files** — no duplication needed.

| What | Copilot (VS Code) | Claude Code | Shared? |
|------|:------------------:|:-----------:|:-------:|
| Agent behavior | ✅ reads `core/` | ✅ reads `core/` | ✅ |
| Skills | ✅ reads `.claude/skills/` | ✅ reads `.claude/skills/` | ✅ |
| Project instructions | ✅ reads `CLAUDE.md` | ✅ reads `CLAUDE.md` | ✅ |
| Agent wrappers | `.github/agents/` | `.claude/agents/` | Separate (different frontmatter) |
| MCP config | `.vscode/mcp.json` | `.mcp.json` | Separate (same server) |

---

## 📁 Repo Structure

```
agents-and-skills/
│
├── setup.py                       ← 🔧 Cross-platform installer (Python)
│
├── core/                          ← 🧠 Agent brains (edit behavior here)
│   └── time-logger/
│       └── prompt.md              ← All time-logger logic lives here
│
├── .claude/
│   ├── agents/
│   │   └── time-logger.md         ← Claude Code wrapper (frontmatter only)
│   └── skills/
│       └── deck/
│           ├── SKILL.md           ← Deck skill instructions
│           ├── recipes.py         ← Python helpers for slide generation
│           └── templates/         ← Your .pptx files go here (gitignored)
│
├── .github/agents/
│   └── time-logger.agent.md       ← Copilot wrapper (frontmatter only)
│
├── .vscode/mcp.json               ← Copilot MCP server config
├── .mcp.json                      ← Claude Code MCP server config
├── CLAUDE.md                      ← Project instructions (both platforms)
└── README.md                      ← You are here
```

> **Key rule:** To change how an agent behaves, edit the file in `core/`. The wrapper files in `.claude/agents/` and `.github/agents/` only contain platform-specific settings — never behavioral logic.

---

## ➕ Add Your Own

### Add a new agent

1. **Write the behavior** in `core/<agent-name>/prompt.md`
2. **Create a Copilot wrapper** at `.github/agents/<agent-name>.agent.md`:
   ```yaml
   ---
   name: "My Agent"
   description: "Use when: ..."
   tools: [relevant-mcp-server/*]
   model: [claude-sonnet-4-5, claude-sonnet-4]
   ---
   Follow the instructions in [core/<agent-name>/prompt.md](../../core/<agent-name>/prompt.md).
   ```
3. **Create a Claude wrapper** at `.claude/agents/<agent-name>.md`:
   ```yaml
   ---
   name: my-agent
   description: "Use when: ..."
   tools: <comma-separated tool names>
   model: sonnet
   ---
   Follow the instructions in [core/<agent-name>/prompt.md](../../core/<agent-name>/prompt.md).
   ```

### Add a new skill

1. Create a folder at `.claude/skills/<skill-name>/`
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) and instructions
3. Optionally add supporting files (scripts, examples)

Both Copilot and Claude Code discover skills from `.claude/skills/` automatically.

---

## ❓ FAQ

<details>
<summary><b>Do I need both VS Code and Claude Code?</b></summary>

No. Use whichever you have. The agents and skills work on either platform independently.
</details>

<details>
<summary><b>I only use VS Code — can I ignore the .claude/ and .mcp.json files?</b></summary>

Yes. VS Code reads from `.claude/agents/` and `.claude/skills/` natively, so those are actually used by both platforms. The only Claude-specific file is `.mcp.json`. Everything else works for you.
</details>

<details>
<summary><b>How do I update an agent's behavior?</b></summary>

Edit the file in `core/<agent-name>/prompt.md`. Both platform wrappers link to it, so the change applies everywhere immediately.
</details>

<details>
<summary><b>The Time Logger agent isn't showing up in Copilot</b></summary>

1. Make sure you have `chat.agent.enabled` turned on in VS Code settings
2. Reload the VS Code window (`Ctrl+Shift+P` → *Reload Window*)
3. Check that the `.github/agents/time-logger.agent.md` file exists
</details>

<details>
<summary><b>Can I add agents/skills without knowing how to code?</b></summary>

Yes! Agents and skills are just Markdown files with instructions written in plain English. The AI reads your instructions and follows them. No programming required — just describe what the agent should do.
</details>

<details>
<summary><b>Are my Azure DevOps tokens stored in the repo?</b></summary>

No. Tokens are entered at runtime via a secure prompt (VS Code) or environment variable (Claude Code). Nothing sensitive is committed. The `.gitignore` blocks settings files and `.env` as a safety net.
</details>

---
