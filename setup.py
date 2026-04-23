#!/usr/bin/env python3
"""
Install agents and skills — globally or into a project.

Auto-discovers all agents and skills from the repo. Adding new ones
requires zero changes to this script.

Usage:
    python setup.py                        # Interactive menu
    python setup.py --global               # Everything, globally
    python setup.py --project /path        # Everything, into a project
    python setup.py --global --copilot     # Only Copilot agents, globally
    python setup.py --uninstall            # Remove everything
"""

import argparse
import json
import os
import platform
import re
import shutil
import sys

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = os.path.dirname(os.path.abspath(__file__))
MARKER = "INSTALLED BY: agents-and-skills"

def _home(*parts):
    return os.path.join(os.path.expanduser("~"), *parts)

def copilot_prompts_dir():
    s = platform.system()
    if s == "Windows":
        return os.path.join(os.environ.get("APPDATA", ""), "Code", "User", "prompts")
    elif s == "Darwin":
        return _home("Library", "Application Support", "Code", "User", "prompts")
    return os.path.join(os.environ.get("XDG_CONFIG_HOME", _home(".config")), "Code", "User", "prompts")

def vscode_settings_path():
    s = platform.system()
    if s == "Windows":
        return os.path.join(os.environ.get("APPDATA", ""), "Code", "User", "settings.json")
    elif s == "Darwin":
        return _home("Library", "Application Support", "Code", "User", "settings.json")
    return os.path.join(os.environ.get("XDG_CONFIG_HOME", _home(".config")), "Code", "User", "settings.json")

CLAUDE_HOME = _home(".claude")

# ---------------------------------------------------------------------------
# Discovery — finds all agents and skills automatically
# ---------------------------------------------------------------------------

def discover_agents():
    """Find all agents by scanning core/ for prompt.md files."""
    agents = []
    core_dir = os.path.join(REPO, "core")
    if not os.path.isdir(core_dir):
        return agents
    for name in sorted(os.listdir(core_dir)):
        core_prompt = os.path.join(core_dir, name, "prompt.md")
        copilot_wrapper = os.path.join(REPO, ".github", "agents", f"{name}.agent.md")
        claude_wrapper = os.path.join(REPO, ".claude", "agents", f"{name}.md")
        if os.path.isfile(core_prompt):
            agents.append({
                "name": name,
                "core": core_prompt,
                "copilot_wrapper": copilot_wrapper if os.path.isfile(copilot_wrapper) else None,
                "claude_wrapper": claude_wrapper if os.path.isfile(claude_wrapper) else None,
            })
    return agents

def discover_skills():
    """Find all skills by scanning .claude/skills/ for SKILL.md files."""
    skills = []
    skills_dir = os.path.join(REPO, ".claude", "skills")
    if not os.path.isdir(skills_dir):
        return skills
    for name in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, name)
        if os.path.isdir(skill_path) and os.path.isfile(os.path.join(skill_path, "SKILL.md")):
            skills.append({"name": name, "path": skill_path})
    return skills

# ---------------------------------------------------------------------------
# Build standalone agent (inline core prompt into wrapper)
# ---------------------------------------------------------------------------

def build_standalone(wrapper_path, core_path, platform_name):
    """Merge wrapper frontmatter + core prompt into a single self-contained file."""
    wrapper = open(wrapper_path, "r", encoding="utf-8").read()
    core = open(core_path, "r", encoding="utf-8").read()

    # Extract YAML frontmatter
    m = re.match(r"(---\n.*?\n---)\n", wrapper, re.DOTALL)
    if not m:
        raise ValueError(f"No frontmatter in {wrapper_path}")

    lines = [f"<!-- {MARKER} | DO NOT EDIT -- reinstall to update -->"]
    lines.append(m.group(1))
    lines.append("")
    lines.append(core)

    if platform_name == "copilot":
        lines.append("")
        lines.append("When the core instructions reference `mcp__azure-devops__*` tool names, "
                      "resolve each one using the `#tool:` prefix for Copilot tool resolution.")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Install functions
# ---------------------------------------------------------------------------

def install_copilot_agents(dest_dir, agents):
    os.makedirs(dest_dir, exist_ok=True)
    for a in agents:
        if not a["copilot_wrapper"]:
            warn(f"No Copilot wrapper for {a['name']}")
            continue
        content = build_standalone(a["copilot_wrapper"], a["core"], "copilot")
        path = os.path.join(dest_dir, f"{a['name']}.agent.md")
        write(path, content)
        ok(f"Copilot agent: {a['name']}")

def install_claude_agents(dest_dir, agents):
    os.makedirs(dest_dir, exist_ok=True)
    for a in agents:
        if not a["claude_wrapper"]:
            warn(f"No Claude wrapper for {a['name']}")
            continue
        content = build_standalone(a["claude_wrapper"], a["core"], "claude")
        path = os.path.join(dest_dir, f"{a['name']}.md")
        write(path, content)
        ok(f"Claude agent: {a['name']}")

def install_skills(dest_dir, skills):
    os.makedirs(dest_dir, exist_ok=True)
    for s in skills:
        dest = os.path.join(dest_dir, s["name"])
        os.makedirs(os.path.join(dest, "templates"), exist_ok=True)
        count = 0
        for root, _, files in os.walk(s["path"]):
            for f in files:
                if f.endswith(".pptx") or f == ".gitkeep":
                    continue
                src = os.path.join(root, f)
                rel = os.path.relpath(src, s["path"])
                dst = os.path.join(dest, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                count += 1
        write(os.path.join(dest, ".installed-by-agents-and-skills"), "installed")
        ok(f"Skill: {s['name']} ({count} files)")

def install_mcp_vscode_global():
    path = vscode_settings_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    settings = {}
    if os.path.isfile(path):
        raw = open(path, "r", encoding="utf-8").read().strip()
        if raw:
            settings = json.loads(raw)

    mcp = settings.setdefault("mcp", {})
    inputs = mcp.setdefault("inputs", [])
    servers = mcp.setdefault("servers", {})

    if not any(i.get("id") == "azure-devops-pat" for i in inputs):
        inputs.append({
            "id": "azure-devops-pat",
            "type": "promptString",
            "description": "Azure DevOps PAT (Work Items R/W, Project and Team Read)",
            "password": True,
        })

    servers["azure-devops"] = {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@azure-devops/mcp", "JKGroupAA"],
        "env": {"AZURE_DEVOPS_EXT_PAT": "${input:azure-devops-pat}"},
    }

    write_json(path, settings)
    ok("MCP: VS Code user settings")

def install_mcp_claude_global():
    path = os.path.join(CLAUDE_HOME, ".mcp.json")
    os.makedirs(CLAUDE_HOME, exist_ok=True)

    config = {}
    if os.path.isfile(path):
        raw = open(path, "r", encoding="utf-8").read().strip()
        if raw:
            config = json.loads(raw)

    servers = config.setdefault("mcpServers", {})
    servers["azure-devops"] = {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@azure-devops/mcp", "JKGroupAA"],
        "env": {"AZURE_DEVOPS_EXT_PAT": "${AZURE_DEVOPS_EXT_PAT}"},
    }

    write_json(path, config)
    ok("MCP: Claude Code global")

def install_mcp_project(project_dir):
    # .vscode/mcp.json
    vsc = os.path.join(project_dir, ".vscode")
    os.makedirs(vsc, exist_ok=True)
    write_json(os.path.join(vsc, "mcp.json"), {
        "inputs": [{"id": "azure-devops-pat", "type": "promptString",
                     "description": "Azure DevOps PAT (Work Items R/W, Project and Team Read)",
                     "password": True}],
        "servers": {"azure-devops": {
            "type": "stdio", "command": "npx",
            "args": ["-y", "@azure-devops/mcp", "JKGroupAA"],
            "env": {"AZURE_DEVOPS_EXT_PAT": "${input:azure-devops-pat}"}}}
    })
    ok("MCP: .vscode/mcp.json")

    # .mcp.json
    write_json(os.path.join(project_dir, ".mcp.json"), {
        "mcpServers": {"azure-devops": {
            "type": "stdio", "command": "npx",
            "args": ["-y", "@azure-devops/mcp", "JKGroupAA"],
            "env": {"AZURE_DEVOPS_EXT_PAT": "${AZURE_DEVOPS_EXT_PAT}"}}}
    })
    ok("MCP: .mcp.json")

# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------

def uninstall():
    header("Uninstalling")

    # Copilot agents
    step("Copilot agents")
    d = copilot_prompts_dir()
    removed = remove_marked_files(d, "*.agent.md")
    if not removed:
        warn("None found")

    # Claude agents
    step("Claude agents")
    d = os.path.join(CLAUDE_HOME, "agents")
    removed = remove_marked_files(d, "*.md")
    if not removed:
        warn("None found")

    # Skills
    step("Skills")
    skills_dir = os.path.join(CLAUDE_HOME, "skills")
    if os.path.isdir(skills_dir):
        for name in os.listdir(skills_dir):
            marker = os.path.join(skills_dir, name, ".installed-by-agents-and-skills")
            if os.path.isfile(marker):
                shutil.rmtree(os.path.join(skills_dir, name))
                ok(f"Removed skill: {name}")

    # MCP
    step("MCP config")
    vsc = vscode_settings_path()
    if os.path.isfile(vsc):
        try:
            s = json.loads(open(vsc, "r", encoding="utf-8").read())
            changed = False
            if "mcp" in s:
                if "servers" in s["mcp"] and "azure-devops" in s["mcp"]["servers"]:
                    del s["mcp"]["servers"]["azure-devops"]
                    changed = True
                if "inputs" in s["mcp"]:
                    s["mcp"]["inputs"] = [i for i in s["mcp"]["inputs"] if i.get("id") != "azure-devops-pat"]
                    if not s["mcp"]["inputs"]:
                        del s["mcp"]["inputs"]
                    changed = True
                if not s["mcp"].get("servers") and not s["mcp"].get("inputs"):
                    del s["mcp"]
            if changed:
                write_json(vsc, s)
                ok("Cleaned VS Code settings")
        except Exception:
            warn("Could not update VS Code settings")

    claude_mcp = os.path.join(CLAUDE_HOME, ".mcp.json")
    if os.path.isfile(claude_mcp):
        try:
            c = json.loads(open(claude_mcp, "r", encoding="utf-8").read())
            if "mcpServers" in c and "azure-devops" in c["mcpServers"]:
                del c["mcpServers"]["azure-devops"]
                if not c["mcpServers"]:
                    os.remove(claude_mcp)
                    ok("Removed empty .mcp.json")
                else:
                    write_json(claude_mcp, c)
                    ok("Cleaned Claude MCP config")
        except Exception:
            warn("Could not update Claude MCP config")

    print("\nDone. Reload VS Code to apply.\n")

def remove_marked_files(directory, pattern):
    import glob
    removed = False
    if not os.path.isdir(directory):
        return False
    for f in glob.glob(os.path.join(directory, pattern)):
        try:
            content = open(f, "r", encoding="utf-8").read()
            if MARKER in content:
                os.remove(f)
                ok(f"Removed {os.path.basename(f)}")
                removed = True
        except Exception:
            pass
    return removed

# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def header(msg):  print(f"\n{'=' * 44}\n   {msg}\n{'=' * 44}")
def step(msg):    print(f"\n>> {msg}")
def ok(msg):      print(f"   [OK] {msg}")
def warn(msg):    print(f"   [--] {msg}")
def fail(msg):    print(f"   [!!] {msg}")

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def ask(prompt, options):
    """Simple numbered menu. Returns the chosen option value."""
    print()
    for i, (label, val) in enumerate(options, 1):
        tag = " (recommended)" if i == 1 else ""
        print(f"  [{i}] {label}{tag}")
    print()
    while True:
        try:
            choice = input(f"  {prompt} ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx][1]
        except (ValueError, EOFError):
            pass
        print(f"  Enter 1-{len(options)}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Install agents and skills.")
    where = parser.add_mutually_exclusive_group()
    where.add_argument("--global", dest="global_", action="store_true", help="Install globally")
    where.add_argument("--project", type=str, help="Install into a project folder")

    what = parser.add_mutually_exclusive_group()
    what.add_argument("--copilot", action="store_true", help="Copilot agents only")
    what.add_argument("--claude", action="store_true", help="Claude agents only")
    what.add_argument("--skills", action="store_true", help="Skills only")
    what.add_argument("--mcp", action="store_true", help="MCP config only")

    parser.add_argument("--uninstall", action="store_true", help="Remove everything")
    parser.add_argument("--skip-mcp", action="store_true", help="Skip MCP config")

    args = parser.parse_args()

    if args.uninstall:
        uninstall()
        return

    # Determine WHERE
    if args.global_:
        mode = "global"
        project_dir = None
    elif args.project:
        mode = "project"
        project_dir = os.path.abspath(args.project)
        if not os.path.isdir(project_dir):
            fail(f"Not a directory: {project_dir}")
            sys.exit(1)
    else:
        # Interactive
        mode = ask("Where do you want to install?", [
            ("Global  - works in every VS Code workspace", "global"),
            ("Project - works in one specific folder", "project"),
            ("Both    - global + a specific project", "both"),
        ])
        project_dir = None
        if mode in ("project", "both"):
            project_dir = input("\n  Project folder path: ").strip()
            if not os.path.isdir(project_dir):
                fail(f"Not a directory: {project_dir}")
                sys.exit(1)
            project_dir = os.path.abspath(project_dir)

    # Determine WHAT
    if args.copilot:
        components = "copilot"
    elif args.claude:
        components = "claude"
    elif args.skills:
        components = "skills"
    elif args.mcp:
        components = "mcp"
    elif args.global_ or args.project:
        components = "all"  # CLI flags = install everything
    else:
        components = ask("What do you want to install?", [
            ("Everything         - agents, skills, and MCP config", "all"),
            ("Copilot agents     - just VS Code / GitHub Copilot", "copilot"),
            ("Claude agents      - just Claude Code", "claude"),
            ("Skills             - just skills (Deck, etc.)", "skills"),
            ("MCP config         - just Azure DevOps server setup", "mcp"),
        ])

    # Discover
    agents = discover_agents()
    skills = discover_skills()

    print(f"\nFound {len(agents)} agent(s), {len(skills)} skill(s)")
    header("Installing")

    do_global = mode in ("global", "both")
    do_project = mode in ("project", "both")

    # Copilot agents
    if components in ("all", "copilot"):
        if do_global:
            step(f"Copilot agents -> {copilot_prompts_dir()}")
            install_copilot_agents(copilot_prompts_dir(), agents)
        if do_project:
            dest = os.path.join(project_dir, ".github", "agents")
            step(f"Copilot agents -> {dest}")
            install_copilot_agents(dest, agents)

    # Claude agents
    if components in ("all", "claude"):
        if do_global:
            dest = os.path.join(CLAUDE_HOME, "agents")
            step(f"Claude agents -> {dest}")
            install_claude_agents(dest, agents)
        if do_project:
            dest = os.path.join(project_dir, ".claude", "agents")
            step(f"Claude agents -> {dest}")
            install_claude_agents(dest, agents)

    # Skills
    if components in ("all", "skills"):
        if do_global:
            dest = os.path.join(CLAUDE_HOME, "skills")
            step(f"Skills -> {dest}")
            install_skills(dest, skills)
        if do_project:
            dest = os.path.join(project_dir, ".claude", "skills")
            step(f"Skills -> {dest}")
            install_skills(dest, skills)

    # MCP
    if components in ("all", "mcp") and not args.skip_mcp:
        if do_global:
            step("MCP -> global config")
            install_mcp_vscode_global()
            install_mcp_claude_global()
        if do_project:
            step(f"MCP -> {project_dir}")
            install_mcp_project(project_dir)

    # Prerequisites check
    step("Prerequisites")
    if shutil.which("node"):
        ok(f"Node.js found")
    else:
        warn("Node.js not found - needed for MCP server (https://nodejs.org/)")

    py = shutil.which("python3") or shutil.which("python")
    if py:
        ok("Python found")
    else:
        warn("Python not found (only needed for Deck skill)")

    # Summary
    print(f"\n{'=' * 44}")
    print("   DONE")
    print(f"{'=' * 44}")
    print()
    print("  Next steps:")
    print("    1. Reload VS Code  (Ctrl+Shift+P > Reload Window)")
    print("    2. Open Copilot Chat  (Ctrl+Alt+I)")
    print("    3. Pick an agent from the dropdown")
    print("    4. Start talking")
    print()
    print("  Update:     git pull && python setup.py --global")
    print("  Uninstall:  python setup.py --uninstall")
    print()

if __name__ == "__main__":
    main()
