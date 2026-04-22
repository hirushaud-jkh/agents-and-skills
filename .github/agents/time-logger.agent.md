---
name: "Time Logger"
description: "Use when: logging hours, filling timesheets, tracking time on Azure DevOps sprint boards, creating or updating work items with time entries, bulk-updating tasks, managing time across multiple Azure DevOps projects, or rolling back time-logging changes."
argument-hint: "Tell me which project and sprint to log time for, or just say 'log time' to start."
tools:
  - azure-devops/*
  - todo
model:
  - claude-sonnet-4-5
  - claude-sonnet-4
---

<!-- COPILOT WRAPPER — Copilot-specific frontmatter only.
     ALL behavioral instructions live in core/time-logger/prompt.md.
     Do NOT add behavioral logic here — edit the core prompt instead. -->

Follow the instructions in [core/time-logger/prompt.md](../../core/time-logger/prompt.md).

When the core instructions reference `mcp__azure-devops__*` tool names, resolve each one using the `#tool:` prefix for Copilot tool resolution. For example, `mcp__azure-devops__core_list_projects` becomes `#tool:mcp__azure-devops__core_list_projects`.
