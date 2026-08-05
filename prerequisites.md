---
layout: default
title: Prerequisites
nav_order: 2
description: Prepare Microsoft Fabric, GitHub Copilot, Rayfin, and local development tools for the labs.
---

# Prerequisites

Complete the shared setup before starting a lab. Initial learners are expected to be Microsoft employees with access to a Microsoft Fabric tenant and a trial or paid Fabric capacity.

{: .important }
Fabric Apps is a preview workload and is not available in every region. Your tenant administrator must enable it before a Fabric App can be created.

## Requirement matrix

| Requirement | Lab 1 | Lab 2 | Lab 3 |
|:------------|:-----:|:-----:|:-----:|
| VS Code and GitHub Copilot Chat | Required | Required | Required |
| Git and Node.js 22 | Required | Required | Required |
| Docker Desktop | Required for local Rayfin | Required for local Rayfin | Not required by the analytics template |
| Capacity-backed Fabric workspace | Required for deployment | Required for deployment | Required |
| Azure CLI | Recommended | Recommended | Required |
| Python 3.11 or later | No | No | Required for model deployment |
| Playwright CLI | No | Recommended | Required |

## 1. Prepare Microsoft Fabric

Ask a Fabric tenant administrator to complete these steps:

1. Open the [Fabric admin portal](https://app.fabric.microsoft.com/admin-portal).
2. Go to **Tenant settings**.
3. Find **Fabric Apps (preview)** and enable it for your organization or your security group.
4. Confirm that your Fabric capacity is in a [region that supports Fabric Apps](https://learn.microsoft.com/fabric/admin/region-availability).

Create or select a workspace at [app.fabric.microsoft.com](https://app.fabric.microsoft.com/) and assign it to a trial or paid Fabric capacity. You need:

- **Contributor** or a higher workspace role to deploy items.
- **Edit** permission on Fabric App items you update.
- **Build** permission on the Lab 3 semantic model.
- **Run and interact** permission for users who test a deployed Fabric App.

Record the workspace ID from the browser address bar. In a workspace URL, it is the GUID after `/groups/`.

## 2. Install developer tools

Install the following software:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/downloads)
- [Node.js 22 LTS](https://nodejs.org/en/download)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Linux containers enabled
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- [Python 3.11 or later](https://www.python.org/downloads/) for Lab 3

Restart the terminal after installing software, then verify it:

```powershell
git --version
node --version
npm --version
docker --version
az version
python --version
```

Node should report version 22. Start Docker Desktop and wait until the engine reports that it is running.

## 3. Configure GitHub Copilot

1. Confirm that your GitHub account has an active [GitHub Copilot plan](https://docs.github.com/copilot/about-github-copilot/plans-for-github-copilot).
2. Install the **GitHub Copilot** and **GitHub Copilot Chat** extensions in VS Code.
3. Sign in to GitHub from VS Code.
4. Open Copilot Chat and confirm that the mode selector offers **Plan** and **Agent** modes. In these labs, Agent mode is referred to as Code mode when it implements an approved plan.

The labs deliberately separate planning from implementation. Review every plan and code change before accepting it, especially authorization rules, schema changes, and generated deployment commands.

## 4. Clone this workshop

```powershell
git clone https://github.com/ahmedbham/rayfin-labs.git
cd rayfin-labs
code .
```

Keep learner applications in sibling folders rather than generating them inside this documentation repository.

## 5. Authenticate to Azure and Fabric

Lab 3 uses the Azure CLI to obtain a token for the Fabric REST API.

```powershell
az login
az account show --output table
az account get-access-token --resource https://api.fabric.microsoft.com --query expiresOn --output tsv
```

If your organization requires a tenant-specific login, use `az login --tenant <tenant-id>`. Never paste access tokens, passwords, publishable keys, or connection strings into Copilot prompts or source files.

## 6. Install Playwright for Lab 3

```powershell
npm install --global @playwright/cli@latest
playwright --version
```

The generated Lab 3 project can instead use a project-local Playwright dependency when its package scripts already provide one.

## 7. Verify readiness

Before starting, confirm that you can:

- Open the capacity-backed workspace in Fabric.
- See Fabric Apps as an available workload or item type.
- Open Copilot Chat in Plan mode and Agent mode.
- Run `docker info` without a daemon connection error for Labs 1 and 2.
- Acquire a Fabric API token with Azure CLI for Lab 3.

{: .checkpoint }
Your environment is ready when every requirement for your chosen lab is installed and the corresponding verification commands succeed.

## Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Fabric Apps does not appear | Confirm the tenant setting, security-group scope, capacity assignment, and supported region. Allow several minutes for a tenant-setting change to propagate. |
| `docker info` cannot connect | Start Docker Desktop and switch to Linux containers. |
| PowerShell cannot find a newly installed command | Close and reopen VS Code so its terminal receives the updated `PATH`. |
| Fabric API returns `401` | Sign in again and request a token for `https://api.fabric.microsoft.com`, not the Power BI API audience. |
| Fabric API returns `403` | Ask for Contributor or higher access to the target workspace. Do not repeatedly retry. |

[Continue to the labs]({% link labs/index.md %}){: .btn .btn-primary }
