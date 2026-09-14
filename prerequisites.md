---
layout: default
title: Prerequisites
nav_order: 2
description: Prepare Microsoft Fabric, GitHub Copilot, Rayfin, and local development tools for the labs.
---

# Prerequisites

Complete the shared setup before starting a lab. Initial learners are expected to be Microsoft employees with access to a Microsoft Fabric tenant and a trial or paid Fabric capacity.

{: .important }
Fabric Apps is a preview workload and is not available in every region.

## Requirement matrix

| Requirement | Lab 1 | Lab 2 | Lab 3 |
|:------------|:-----:|:-----:|:-----:|
| GitHub Codespaces | Recommended | Recommended | Recommended |
| VS Code and GitHub Copilot Chat | Required | Required | Required |
| Git and Node.js 22 | Required | Required | Required |
| Rayfin CLI (`@microsoft/rayfin-cli`) | Required | Required if prompted by the lab | Required |
| Docker Desktop | Required for local Rayfin | Not required by the analytics template | Required for local Rayfin |
| Capacity-backed Fabric workspace | Required for deployment | Required | Required for deployment |
| Azure CLI | Recommended | Required | Recommended |
| Python 3.11 or later | No | Required for model deployment | No |
| Playwright CLI | No | Required | Recommended |

When using GitHub Codespaces, only Azure CLI is required from the developer tools listed in this matrix. The remaining developer tool requirements apply to local development.

## 1. Prepare Microsoft Fabric

Complete these steps in Microsoft Fabric:

1. Open [Microsoft Fabric](https://app.fabric.microsoft.com/).
2. At the bottom left, if **Power BI** is displayed, select it and switch to **Fabric**.
3. Select **My workspace** from the left menu.
4. Select **Workspace settings** from the top right.
5. Under **Workspace type**, ensure that **Fabric Trial** is selected and a trial capacity is assigned to the workspace. All lab artifacts will be deployed to this workspace.

Record the workspace ID from the browser address bar. In a workspace URL, it is the GUID after `/groups/`.

## 2. Install developer tools

Install the following software (if not using GH Codespaces):

- [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/downloads)
- [Node.js 22 LTS](https://nodejs.org/en/download)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Linux containers enabled
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- [Python 3.11 or later](https://www.python.org/downloads/) for Lab 2

Restart the terminal after installing software, then verify it:

```bash
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

## 4. Install the Rayfin CLI

The Rayfin CLI is distributed as the `@microsoft/rayfin-cli` npm package. Verify that Node.js 22 and npm are available:

```bash
node --version
npm --version
```

Install Rayfin CLI version 1.34.0 globally, then verify the installation. The labs pin this version because later versions change the browser callback behavior used in GitHub Codespaces.

```bash
npm install --global @microsoft/rayfin-cli@1.34.0
rayfin --version
```

The version command should report `1.34.0`.

Sign in to Rayfin using your Microsoft Entra tenant ID:

```bash
rayfin login -t <tenant-id>
```

If your environment cannot use the operating system credential store, enable encrypted file-based credential storage:

```bash
rayfin login -t <tenant-id> --encryption-fallback-enabled
```

Keep the tenant ID and other environment-specific values out of source control.

## 5. Fork and open this workshop

Using a GitHub Codespace created from your own fork is recommended. The fork gives you a repository where you can commit and push your lab work without needing write access to the workshop repository.

1. Sign in to GitHub and open the [rayfin-labs repository](https://github.com/ahmedbham/rayfin-labs).
2. Select **Fork** in the top-right corner.
3. Choose your GitHub account as the owner, keep the default repository name, and select **Create fork**.
4. In your fork, select **Code**, then select the **Codespaces** tab.
5. Select **Create codespace on main**.
6. Wait for the Codespace to open in the browser-based VS Code editor.

Your Codespace is connected to your fork, so you can commit and push changes as you complete the labs.

For local development, clone your fork instead:

```bash
git clone https://github.com/<github-username>/rayfin-labs.git
cd rayfin-labs
code .
```

For local development, keep learner applications in sibling folders rather than generating them inside this documentation repository. In Codespaces, create learner applications in dedicated folders within your fork so that you can commit and push them.

## Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Fabric Apps does not appear | Confirm the tenant setting, security-group scope, capacity assignment, and supported region. Allow several minutes for a tenant-setting change to propagate. |
| `docker info` cannot connect | Start Docker Desktop and switch to Linux containers. |
| bash cannot find a newly installed command | Close and reopen VS Code so its terminal receives the updated `PATH`. |
| bash finds `az`, but the Python deployment helper does not | Run `python -c "import shutil; print(shutil.which('az'))"`. On Windows, it should print the full path to `az.CMD`; if it prints `None`, fully close and reopen VS Code so Python receives the updated `PATH` and `PATHEXT`. |
| Fabric API returns `401` | Sign in again and request a token for `https://api.fabric.microsoft.com`, not the Power BI API audience. |
| Fabric API returns `403` | Ask for Contributor or higher access to the target workspace. Do not repeatedly retry. |

[Continue to the labs]({% link labs/index.md %}){: .btn .btn-primary }
