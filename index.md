---
layout: default
title: Build Fabric Apps with Rayfin
nav_order: 1
description: Three hands-on labs for building Microsoft Fabric Apps with Rayfin CLI and GitHub Copilot.
permalink: /
---

# Build Fabric Apps with Rayfin

Build data-driven applications on Microsoft Fabric using Rayfin CLI and GitHub Copilot. These hands-on labs progress from a guided local application to requirements-driven and analytics-focused Fabric Apps.

{: .warning }
Fabric Apps and full local Rayfin development are preview or experimental experiences. Commands and generated project structures can change.

## Workshop path

| Lab | Scenario | What you practice |
|:----|:---------|:------------------|
| 1 | Todo application | Scaffold, run, modify, test, and deploy a Rayfin application. |
| 2 | Interactive operations dashboard | Build a cross-filterable application over a Power BI semantic model. |
| 3 | Field technician application | Use Copilot Plan mode and Code mode to implement detailed functional requirements with a SQL database in Fabric. |

Start with the [prerequisites]({% link prerequisites.md %}), even if you already use Microsoft Fabric. The setup page separates requirements by lab so you can install only what you need.

## Architecture progression

```text
Lab 1: React UI -> Rayfin typed client -> local Docker services -> Fabric App
Lab 2: Interactive visuals -> semantic model queries -> Power BI semantic model
Lab 3: Role-aware UI -> generated GraphQL API -> SQL database in Fabric
```

Each lab includes checkpoints, executable validation, cloud deployment, troubleshooting, and cleanup.
