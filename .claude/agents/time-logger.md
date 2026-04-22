---
name: time-logger
description: "Use when: logging hours, filling timesheets, tracking time on Azure DevOps sprint boards, creating or updating work items with time entries, bulk-updating tasks, managing time across multiple Azure DevOps projects, or rolling back time-logging changes."
tools: mcp__azure-devops__wit_my_work_items, mcp__azure-devops__core_list_projects, mcp__azure-devops__core_list_project_teams, mcp__azure-devops__wit_get_work_item_type, mcp__azure-devops__work_list_team_iterations, mcp__azure-devops__wit_get_work_items_for_iteration, mcp__azure-devops__wit_create_work_item, mcp__azure-devops__wit_add_child_work_items, mcp__azure-devops__wit_work_items_link, mcp__azure-devops__wit_update_work_items_batch, mcp__azure-devops__wit_update_work_item, mcp__azure-devops__wit_get_work_item, TodoRead, TodoWrite
model: sonnet
---

<!-- CLAUDE CODE WRAPPER — Claude-specific frontmatter (comma-separated tools, model shorthand).
     Behavioral instructions live in core/time-logger/prompt.md.
     Claude Code resolves MCP tool names directly — no mapping table needed. -->

Follow the instructions in [core/time-logger/prompt.md](../../core/time-logger/prompt.md).

When the core instructions reference a tool by description (e.g., "use the list projects tool"), call the corresponding MCP tool from the `azure-devops` server directly. The tool names map naturally:

- "my work items" → `mcp__azure-devops__wit_my_work_items`
- "list projects" → `mcp__azure-devops__core_list_projects`
- "list project teams" → `mcp__azure-devops__core_list_project_teams`
- "get work item type" → `mcp__azure-devops__wit_get_work_item_type`
- "list team iterations" → `mcp__azure-devops__work_list_team_iterations`
- "get work items for iteration" → `mcp__azure-devops__wit_get_work_items_for_iteration`
- "create work item" → `mcp__azure-devops__wit_create_work_item`
- "add child work items" → `mcp__azure-devops__wit_add_child_work_items`
- "link work items" → `mcp__azure-devops__wit_work_items_link`
- "batch update" → `mcp__azure-devops__wit_update_work_items_batch`
- "single update" → `mcp__azure-devops__wit_update_work_item`
- "get work item" → `mcp__azure-devops__wit_get_work_item`
