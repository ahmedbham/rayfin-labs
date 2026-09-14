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
| Laptop with VS Code | Recommended | Recommended | Recommended |
| GitHub Codespaces | Supported | Supported | Supported |
| VS Code and GitHub Copilot Chat | Required | Required | Required |
| Git and Node.js 22 | Required | Required | Required |
| Rayfin CLI (`@microsoft/rayfin-cli`) | Required | Required if prompted by the lab | Required |
| Docker Desktop | Required for local Rayfin | Not required by the analytics template | Required for local Rayfin |
| Capacity-backed Fabric workspace | Required for deployment | Required | Required for deployment |
| Azure CLI | Recommended | Required | Recommended |
| Python 3.11 or later | No | Required for model deployment | No |
| Playwright CLI | No | Required | Recommended |

Running the labs on a laptop is recommended because browser authentication, Docker networking, and local callbacks work directly. GitHub Codespaces is also supported; verify the same command-line tools in the Codespace and use the documented callback workaround when a browser cannot reach `localhost` in the container.

## 1. Prepare Microsoft Fabric

Complete these steps in Microsoft Fabric:

1. Open [Microsoft Fabric](https://app.fabric.microsoft.com/).
2. At the bottom left, if **Power BI** is displayed, select it and switch to **Fabric**.
3. Select **My workspace** from the left menu.
4. Select **Workspace settings** from the top right.
5. Under **Workspace type**, ensure that **Fabric Trial** is selected and a trial capacity is assigned to the workspace. All lab artifacts will be deployed to this workspace.

## 2. Install developer tools

Install the following software on your laptop. In GitHub Codespaces, most tools are preinstalled, but you must still verify them and install Azure CLI if it is missing:

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

Remove Rayfin CLI version 1.35.0 if it is installed, then install version 1.34.0 globally and verify the installation. The labs pin this version because version 1.35.0 changes the browser callback behavior used in GitHub Codespaces.

```bash
npm uninstall --global @microsoft/rayfin-cli@1.35.0
npm install --global @microsoft/rayfin-cli@1.34.0
rayfin --version
```

The version command should report `1.34.0`.

On a laptop, authenticate Azure CLI against your Microsoft Entra tenant before running a lab:

```bash
az login -t <tenant-id>
```

Before running Rayfin CLI commands on either a laptop or in Codespaces, authenticate the pinned Rayfin CLI:

```bash
rayfin login -t <tenant-id>
```

If a generated template specifically instructs you to run `rayfin auth`, first confirm that its installed CLI exposes that command with `rayfin help`, then run:

```bash
rayfin auth
```

Complete each browser prompt with the same tenant account. In Codespaces, use `rayfin login -t <tenant-id> --encryption-fallback-enabled`; if the browser callback cannot reach `localhost`, copy the complete callback URL from the browser and run `curl "<copied-url>"` in a second Codespaces terminal. Keep the tenant ID and other environment-specific values out of source control.

## 5. Fork and open this workshop

Running the workshop from a laptop is recommended. Fork the repository first so you can commit and push your lab work without needing write access to the workshop repository.

1. Sign in to GitHub and open the [rayfin-labs repository](https://github.com/ahmedbham/rayfin-labs).
2. Select **Fork** in the top-right corner.
3. Choose your GitHub account as the owner, keep the default repository name, and select **Create fork**.
4. Clone your fork to your laptop and open the repository root in VS Code:

```bash
git clone https://github.com/<github-username>/rayfin-labs.git
cd rayfin-labs
code .
```

To use GitHub Codespaces instead, open your fork, select **Code** > **Codespaces** > **Create codespace on main**, and wait for the browser-based VS Code editor to open.

For every lab, begin in this repository root. Run `rayfin init` here when the command creates the project folder, or create the lab's project folder here when the lab explicitly requires an empty directory. Do not create a sibling projects directory or leave the cloned repository before scaffolding.

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
