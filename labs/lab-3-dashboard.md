---
layout: default
title: "Lab 3: Interactive dashboard"
parent: Labs
nav_order: 3
description: Use GitHub Copilot to build a cross-filterable Fabric App over a Power BI semantic model.
---

# Lab 3: Build an interactive dashboard

**Estimated time:** 90-120 minutes

In this lab, you deploy the bundled Contoso semantic model and use GitHub Copilot to plan and implement an interactive Fabric App. Unlike a static dashboard, selections are shared across compatible visuals so users can explore operational relationships.

## Objectives

- Deploy a local TMDL semantic model reproducibly through the Fabric REST API.
- Ground a Copilot plan in real tables, measures, columns, and relationships.
- Implement shared filters and cross-filtering with resilient UI states.
- Validate desktop/mobile behavior and deploy the analytics app to Fabric.

## Before you begin

Complete the [prerequisites]({% link prerequisites.md %}). Lab 3 requires Azure CLI and Rayfin authentication, Python 3.11 or later, Node.js and npm, a capacity-backed Fabric workspace, and Playwright.

Running this lab on a laptop is recommended. From the repository root, authenticate Azure CLI and Rayfin with the same Microsoft Entra tenant account:

```bash
az login -t <tenant-id>
rayfin login -t <tenant-id>
```

If the generated template specifically requires `rayfin auth` and `rayfin help` lists it, run that command as well. GitHub Codespaces is also supported: run `rayfin login -t <tenant-id> --encryption-fallback-enabled`; if the browser cannot reach its `localhost:` callback, copy the complete callback URL and run `curl "<copied-url>"` in a second Codespaces terminal.

Open these workshop assets:

- [Dashboard prompt](https://github.com/ahmedbham/rayfin-labs/blob/main/lab-assets/lab-2/LAB_2_PROMPT.md)
- [Contoso semantic model](https://github.com/ahmedbham/rayfin-labs/tree/main/lab-assets/lab-2/Contoso-DT-Dashboard.SemanticModel)
- [Semantic model deployment helper](https://github.com/ahmedbham/rayfin-labs/blob/main/scripts/deploy_semantic_model.py)
- [Create an app connected to a semantic model](https://learn.microsoft.com/en-us/fabric/apps/data-apps-template?source=recommendations)

## Exercise 1: Deploy the semantic model

From this workshop repository, validate the model package without connecting to Fabric:

```bash
python scripts/deploy_semantic_model.py --dry-run
```

The command should list 10 parts: `definition.pbism`, database/model/relationship definitions, and six table definitions.

Deploy the model. Replace the placeholder with the workspace GUID or exact display name recorded during setup:

```bash
python scripts/deploy_semantic_model.py --workspace-id <workspace-id-or-name>
```

The helper verifies capacity assignment, obtains a Fabric-scoped access token from Rayfin's authentication cache, packages each TMDL file as inline base64, polls asynchronous operations, and prints the semantic model ID. It does not persist the token.

If a model named **Contoso DT Dashboard** already exists and you intentionally want to replace its complete definition, use:

```bash
python scripts/deploy_semantic_model.py --workspace-id <workspace-id-or-name> --update-existing
```

{: .warning }
`--update-existing` replaces the complete semantic-model definition. Use it only for the model created by this lab and never against an unrelated production model.

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

Follow the current Microsoft Learn instructions in [Create an app connected to a semantic model](https://learn.microsoft.com/en-us/fabric/apps/data-apps-template?source=recommendations). Return to this workshop repository root, then run:

```bash
rayfin init "<appitemname>" --template dataapp --workspace <workspacename>
```

Replace `<appitemname>` with a unique Fabric App item name, such as `contoso-dt-dashboard-app`, and replace `<workspacename>` with the exact display name of the workspace containing the semantic model. Keep the quotation marks around the app item name when it contains spaces.

When the command finishes, change to the generated app directory and open it in Visual Studio Code:

```bash
cd "<appitemname>"
code .
```

{: .checkpoint }
The generated data app project is open in Visual Studio Code and the Fabric App item appears in the target workspace.

## Exercise 3: Build with GitHub Copilot

In Visual Studio Code, open GitHub Copilot Chat and select **Agent** mode. Paste the following prompt, replacing the example semantic model URL with the complete URL you stored in Exercise 1:

```text
Build a [Microsoft Fabric App](https://learn.microsoft.com/fabric/apps/overview) using [Rayfin CLI](https://github.com/microsoft/rayfin) as an interactive, cross-filterable interface to the Power BI semantic model at https://msit.powerbi.com/groups/workspace-id/modeling/model-id/modelView

Before writing code, inspect the semantic model's tables, measures, columns, and relationships and produce an implementation plan that maps every proposed visual to real model fields or measures. Include KPI summaries and analytical views for operational metrics, investment, initiatives, asset visibility, and AI detections.
```

Copilot can use the model URL to identify the workspace and semantic model. Let Agent mode inspect the generated template and model metadata, then review its plan before approving implementation.

### Review rubric

Approve the plan only when it includes:

| Area | Expected coverage |
|:-----|:------------------|
| Executive summary | Latest availability, MTTR, incidents, change success, security, and service KPIs using existing measures. |
| Trends | Date-aware incident, disruption, MTTR, change, or security trends that respect the selected period. |
| Portfolio | Investment by business unit/theme and initiatives by status/off-track state. |
| Risk and AI | Asset visibility by severity and AI detections by system/severity. |
| Query mapping | Each visual names real tables, columns, measures, grouping, sorting, and filter inputs. |
| Interactions | Date, business unit, theme, status, severity, and system selections update only compatible visuals; reset restores defaults. |
| State model | Initial loading, per-query failure, empty result, partial data, retry, stale request cancellation, and no-selection behavior. |
| Quality | Keyboard operation, focus indication, text alternatives, color-independent status, responsive layout, tests, and Playwright checks. |

Avoid a plan that loads the full dataset into the browser or simulates filtering only on already-rendered values. Preserve the data app template's semantic-model query abstraction and issue appropriately filtered and aggregated queries.

{: .checkpoint }
Every visual maps to real model metadata, and the approved plan defines shared filters, compatible interactions, query behavior, and executable tests.

## Exercise 4: Implement and validate locally

Ask Copilot Agent to implement the approved plan. Keep the data app template's Fabric authentication, semantic-model connectivity, visualization primitives, formatting, and query patterns intact. Do not invent model fields, hard-code credentials, or load the full dataset into the browser.

Use this implementation order:

1. Runtime configuration and semantic-model client wiring.
2. Typed query definitions and result transformations.
3. Shared filter state, compatibility rules, reset, and stale-request cancellation.
4. KPI and trend views.
5. Investment, initiative, asset visibility, and AI detection views.
6. Loading, empty, partial-error, retry, and no-selection states.
7. Keyboard/accessibility behavior and responsive layout.
8. Automated tests and Playwright browser scenarios.

After each phase, have Copilot run the narrowest available validation. Measure names containing spaces or punctuation must be referenced exactly as exposed by the semantic model.

Run the generated project's lint, test, and production build commands. Use the scripts defined in its `package.json`; these are typically:

```bash
npm run lint
npm run test
npm run build
```

Ask Copilot to use the template's Playwright browser-validation workflow to check initial rendering, cross-filtering, reset behavior, errors, and desktop/mobile layout. Inspect the screenshots rather than treating a successful element lookup as visual proof.

## Exercise 5: Preview in the Fabric shell

Start the local frontend using the command documented by the generated template, typically:

```bash
npm run dev
```

Navigate to the target workspace in the Fabric portal and open the Fabric App artifact created for local development. Append the development URI to its browser URL:

```text
&devUri=http://localhost:5173
```

Use the exact URL printed by Vite if it selects another port. The Fabric shell supplies the brokered context expected by the starter.

Validate these interactions manually:

1. Select a date period and confirm related metrics and AI detections update.
2. Select an investment business unit and confirm compatible portfolio visuals update without incorrectly filtering unrelated metric tables.
3. Select severity in asset or AI views and confirm compatible risk visuals respond.
4. Combine two compatible filters and verify visible filter context is clear.
5. Reset filters and confirm the default dashboard returns.
6. Force or simulate one query failure and confirm other successful sections remain useful.

{: .checkpoint }
Lint, unit/component tests, production build, and browser checks pass; desktop and mobile screenshots show a usable, nonblank dashboard.

## Exercise 6: Deploy and verify the Fabric App

From the generated app directory, deploy the app to Fabric with Rayfin:

```bash
rayfin up
```

Wait for the command to complete successfully. In the Fabric portal, open the target workspace, select the Fabric App item created in Exercise 2, and verify that the latest build is available inside the Fabric portal.

After deployment:

1. Open the app inside the Fabric portal and verify that it renders without a separate sign-in prompt.
2. Confirm the deployed app queries the intended semantic model ID.
3. Repeat one cross-filter and reset scenario.
4. Test with a user who has **Run and interact** on the app and **Build** permission on the semantic model.
5. Confirm no token or credential appears in source, generated JavaScript, browser storage, or network query parameters.

{: .note }
Semantic-model-connected Fabric Apps currently must run inside the Fabric portal. Opening the app in a standalone browser window can cause visual queries to fail.

{: .checkpoint }
The Rayfin deployment succeeds, the latest app build opens in the Fabric portal, live semantic-model data renders, and cross-filter and reset interactions work.

## Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Helper returns `401` | On a laptop, run `az login -t <tenant-id>`, then `rayfin login -t <tenant-id>`. In Codespaces, add `--encryption-fallback-enabled` to the Rayfin login. If the project explicitly requires `rayfin auth` and lists it in `rayfin help`, run that too. |
| Helper returns `403` | Stop and obtain Contributor or higher workspace access. |
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

[Previous: Lab 2]({% link labs/lab-2-field-technician.md %}){: .btn }
[Back to labs]({% link labs/index.md %}){: .btn .btn-primary }
