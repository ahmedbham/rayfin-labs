---
layout: default
title: "Lab 2: Interactive dashboard"
parent: Labs
nav_order: 2
description: Use GitHub Copilot to build a cross-filterable Fabric App over a Power BI semantic model.
redirect_from:
  - /labs/lab-3-dashboard.html
---

# Lab 2: Build an interactive dashboard

**Estimated time:** 90-120 minutes

In this lab, you deploy the bundled Contoso semantic model and use GitHub Copilot to plan and implement an interactive Fabric App. Unlike a static dashboard, selections are shared across compatible visuals so users can explore operational relationships.

## Objectives

- Deploy a local TMDL semantic model reproducibly through the Fabric REST API.
- Ground a Copilot plan in real tables, measures, columns, and relationships.
- Implement shared filters and cross-filtering with resilient UI states.
- Validate desktop/mobile behavior and deploy the analytics app to Fabric.

## Before you begin

Complete the [prerequisites]({% link prerequisites.md %}) and [Lab 1]({% link labs/lab-1-todo.md %}). Lab 2 requires an authenticated Rayfin CLI, Python 3.11 or later, Node.js and npm, a capacity-backed Fabric workspace, and Playwright.

Open these workshop assets:

- [Lab 2 prompt](https://github.com/ahmedbham/rayfin-labs/blob/main/lab-assets/lab-2/LAB_2_PROMPT.md)
- [Contoso semantic model](https://github.com/ahmedbham/rayfin-labs/tree/main/lab-assets/lab-2/Contoso-DT-Dashboard.SemanticModel)
- [Semantic model deployment helper](https://github.com/ahmedbham/rayfin-labs/blob/main/scripts/deploy_semantic_model.py)
- [Create an app connected to a semantic model](https://learn.microsoft.com/en-us/fabric/apps/data-apps-template?source=recommendations)

## Exercise 1: Deploy the semantic model

- change directory to the workshop repository where the semantic model and deployment helper are located.

```bash
cd "lab-assets/lab-2"
```

- Validate the model package without connecting to Fabric.

```bash
python scripts/deploy_semantic_model.py --dry-run
```

The command should list 10 parts: `definition.pbism`, database/model/relationship definitions, and six table definitions.

- Set your Microsoft Entra tenant ID and sign in to Rayfin:

	```bash
	RAYFIN_TENANT_ID=<tenant-guid>
	rayfin login -t $RAYFIN_TENANT_ID --encryption-fallback-enabled
	```

- Complete sign-in in the browser. If the browser opens a page showing **Hmmm... can't reach this page**:
	- Copy the complete URL from the page. It starts with `localhost:`.
	- Open a new terminal in the Codespace.
	- Run the callback URL through `curl`:

	  ```bash
	  curl "<copied-url>"
	  ```

- Return to the original terminal and deploy the app to Fabric:

	```bash
	python scripts/deploy_semantic_model.py --workspace-id <workspace-id-or-name>
	```

The helper verifies capacity assignment, obtains a Fabric-scoped access token from Rayfin's login cache, packages each TMDL file as inline base64, polls asynchronous definition operations, and prints the semantic model ID. It does not persist the token.

If a model named **Contoso DT Dashboard** already exists and you intentionally want to replace its complete definition, use:

```bash
python scripts/deploy_semantic_model.py --workspace-id <workspace-id-or-name> --update-existing
```

{: .warning }
`--update-existing` replaces the complete semantic-model definition. Use it only for the model created by this lab and never against an unrelated production model.

After deployment, open the semantic model in Fabric and select **Refresh now**. Wait for the refresh history to report **Completed** before previewing a table. The Fabric REST API does not currently expose a refresh job for semantic model items.

Open the model in the Fabric workspace and confirm these tables:

| Table | Analytical role |
|:------|:----------------|
| `Date` | Month and date filtering for related time-series facts. |
| `Metrics` | Availability, incident, change, security, service, and AI solution KPIs and trends. |
| `Investment` | Investment by business unit and strategic theme. |
| `Initiatives` | Initiative status, business unit, and off-track indicators. |
| `AssetVisibility` | Covered and total assets by severity. |
| `AIDetections` | Claims and provider AI detections by date and severity. |

Record the semantic model ID printed by the helper. It is also the dataset ID used by Power BI APIs.

In the Fabric portal, select **Contoso DT Dashboard** to open the semantic model. Copy the complete URL from the browser address bar and store it for the app-building prompt. It has this form:

```text
https://msit.powerbi.com/groups/workspace-id/modeling/model-id/modelView
```

Keep the actual workspace and model IDs in the copied URL. Do not use the placeholder URL in the later prompt.

{: .checkpoint }
The model appears in the target workspace, all six tables are present, and you have stored its complete model URL for later use.

## Exercise 2: Create the Fabric data app

Follow the current Microsoft Learn instructions in [Create an app connected to a semantic model](https://learn.microsoft.com/en-us/fabric/apps/data-apps-template?source=recommendations). From the parent folder where you keep projects (for example, `cd "$GITHUB_WORKSPACE"` in Codepace), run

```bash
rayfin init "<appitemname>" --template dataapp --workspace <workspacename>
```

Replace `<appitemname>` with a unique Fabric App item name, such as `contoso-dt-dashboard-app`, and replace `<workspacename>` with the exact display name of the workspace containing the semantic model. Keep the quotation marks around the app item name when it contains spaces.

When the command finishes, change to the generated app directory

```bash
cd "<appitemname>"
```

## Exercise 3: Build with GitHub Copilot

Open GitHub Copilot Chat and select **Agent** mode. Paste the following prompt, replacing the example semantic model URL with the complete URL you stored in Exercise 1:

```text
Update Fabric app **my-lab2-dt-app** as an interactive, cross-filterable interface to the Power BI semantic model at "https://msit.powerbi.com/groups/workspace-id/modeling/model-id/modelView". For reference, **dt-dashboard-report-image.png** is a screenshot of a Power Bi report on this semantic model.   
```

Copilot can use the model URL to identify the workspace and semantic model. 

## Exercise 4: Deploy and verify the Fabric App

From the generated app directory, deploy the app to Fabric with Rayfin:

```bash
rayfin up
```

Wait for the command to complete successfully. In the Fabric portal, open the target workspace, select the Fabric App item created in Exercise 2, and verify that the latest build is available inside the Fabric portal.

After deployment:

1. Open the app inside the Fabric portal and verify that it renders without a separate sign-in prompt.
2. Confirm the deployed app queries the intended semantic model ID.
3. Repeat one cross-filter and reset scenario.

{: .checkpoint }
The Rayfin deployment succeeds, the latest app build opens in the Fabric portal, live semantic-model data renders, and cross-filter and reset interactions work.

## Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Helper returns `401` | Run `rayfin login -t <tenant-id> --encryption-fallback-enabled` again. The helper requests Rayfin's default Fabric scope. |
| Helper returns `403` | Stop and obtain Contributor or higher workspace access. |
| Tables contain no data after deployment | Select **Refresh now** for the semantic model and wait for refresh history to report **Completed**. |
| Helper reports no capacity | Assign the workspace to a supported Fabric capacity before retrying. |
| Rayfin cannot create the app item | Confirm the Fabric Apps workload is enabled and that you are a workspace Contributor or Admin. |
| Visual queries return permission errors | Confirm the Semantic Model Execute Queries REST API tenant setting is enabled and the user has Build and Read permissions on the model. |
| A query reports an unknown field or measure | Compare its exact name and table with the local TMDL; do not guess aliases. |
| Local page is blank outside Fabric | Use the Fabric shell URL with `devUri` so brokered authentication/context is available. |
| Deployed visuals fail in a standalone window | Open the Fabric App from its workspace in the Fabric portal. Standalone opening is currently unsupported for semantic-model-connected apps. |
| Filters race and show stale results | Cancel or disregard older requests when filter state changes. Add a regression test. |

## Clean up

Delete the deployed Fabric App when finished. Delete **Contoso DT Dashboard** only if it was created specifically for this lab and is not used by another app or report.

## Completion criteria

- The bundled TMDL model is reproducibly deployed and its complete model URL is stored.
- The approved plan maps every visual to real model metadata.
- Compatible visuals cross-filter through shared state and reset correctly.
- Robust states, keyboard access, and responsive layouts are validated.
- All automated checks pass and the deployed app works inside the Fabric portal through Fabric SSO.

[Previous: Lab 1]({% link labs/lab-1-todo.md %}){: .btn }
[Next: Lab 3]({% link labs/lab-3-field-technician.md %}){: .btn .btn-primary }
