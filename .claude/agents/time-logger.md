---
name: time-logger
description: "Use when: logging hours, filling timesheets, tracking time on Azure DevOps sprint boards, creating or updating work items with time entries, bulk-updating tasks, managing time across multiple Azure DevOps projects, or rolling back time-logging changes."
tools: mcp__azure-devops__wit_my_work_items, mcp__azure-devops__core_list_projects, mcp__azure-devops__core_list_project_teams, mcp__azure-devops__wit_get_work_item_type, mcp__azure-devops__work_list_team_iterations, mcp__azure-devops__wit_get_work_items_for_iteration, mcp__azure-devops__wit_create_work_item, mcp__azure-devops__wit_add_child_work_items, mcp__azure-devops__wit_work_items_link, mcp__azure-devops__wit_update_work_items_batch, mcp__azure-devops__wit_update_work_item, mcp__azure-devops__wit_get_work_item, TodoRead, TodoWrite
model: sonnet
---

<!-- CLAUDE CODE WRAPPER — Claude-specific frontmatter only.
     ALL behavioral instructions live in core/time-logger/prompt.md.
     Do NOT add behavioral logic here — edit the core prompt instead. -->

Follow the instructions in [core/time-logger/prompt.md](../../core/time-logger/prompt.md).

The core instructions use `mcp__azure-devops__*` tool names directly — call them as-is.
