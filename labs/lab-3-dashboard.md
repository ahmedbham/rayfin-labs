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

Complete the [prerequisites]({% link prerequisites.md %}). Lab 3 requires Azure CLI authentication, Python 3.11 or later, a capacity-backed Fabric workspace, and Playwright.

Open these workshop assets:

- [Lab 3 prompt](https://github.com/ahmedbham/rayfin-labs/blob/main/LAB_3_PROMPT.md)
- [Contoso semantic model](https://github.com/ahmedbham/rayfin-labs/tree/main/Contoso-DT-Dashboard.SemanticModel)
- [Semantic model deployment helper](https://github.com/ahmedbham/rayfin-labs/blob/main/scripts/deploy_semantic_model.py)

## Exercise 1: Deploy the semantic model

From this workshop repository, validate the model package without connecting to Fabric:

```powershell
python scripts/deploy_semantic_model.py --dry-run
```

The command should list 10 parts: `definition.pbism`, database/model/relationship definitions, and six table definitions.

Sign in and deploy the model. Replace the placeholder with the workspace GUID recorded during setup:

```powershell
az login
python scripts/deploy_semantic_model.py --workspace-id <workspace-id>
```

The helper verifies capacity assignment, obtains a Fabric-scoped access token from Azure CLI, packages each TMDL file as inline base64, polls asynchronous operations, and prints the semantic model ID. It does not persist the token.

If a model named **Contoso DT Dashboard** already exists and you intentionally want to replace its complete definition, use:

```powershell
python scripts/deploy_semantic_model.py --workspace-id <workspace-id> --update-existing
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

{: .checkpoint }
The model appears in the target workspace, all six tables are present, and you have its semantic model ID.

## Exercise 2: Prepare the analytics starter

In a sibling projects folder, clone the code-sample template:

```powershell
git clone https://github.com/ahmedbham/rayfin-nyc-taxi-app.git contoso-dt-dashboard-app
cd contoso-dt-dashboard-app
npm install
code .
```

Copy `LAB_3_PROMPT.md` and the `Contoso-DT-Dashboard.SemanticModel` folder from this workshop into a temporary `requirements/` folder in the starter project. The model copy gives Copilot local schema context; the deployed workspace model remains the runtime source.

Inspect the starter's `README.md`, `AGENTS.md`, `.agents/skills/`, `fabric.yaml`, semantic-model query services, authentication setup, package scripts, and tests. Follow the starter's current environment-variable pattern for workspace and semantic model IDs.

Do not commit environment files containing IDs or tokens. A workspace/model GUID is not a password, but keeping environment-specific configuration outside source makes the app portable and prevents accidental tenant coupling.

## Exercise 3: Plan with Copilot

Open Copilot Chat in **Plan** mode. Attach `requirements/LAB_3_PROMPT.md`, the semantic model `definition/model.tmdl`, `definition/relationships.tmdl`, and all table TMDL files. Enter:

> Follow `LAB_3_PROMPT.md`. Inspect this analytics starter and the complete local TMDL model. Produce an ordered implementation plan without editing files. Include a visual-to-model mapping, query strategy, shared filter-state design, cross-filter interaction matrix, component and test plan, responsive behavior, and focused validation after each phase. Flag any visual that cannot be supported by an existing field or measure.

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

Avoid a plan that loads the full dataset into the browser or simulates filtering only on already-rendered values. Prefer the starter's semantic-model query abstraction and issue appropriately filtered/aggregated queries.

{: .checkpoint }
Every visual maps to real model metadata, and the approved plan defines shared filters, compatible interactions, query behavior, and executable tests.

## Exercise 4: Implement in Code mode

Switch Copilot to **Agent** mode and enter:

> Implement the approved plan one phase at a time, preserving the starter's Fabric authentication and query abstractions. Begin with typed filter state, query definitions, and focused tests. After each phase, run the narrowest validation and stop for review. Do not invent model fields or hard-code credentials and semantic model IDs.

Use this implementation order:

1. Runtime configuration and semantic-model client wiring.
2. Typed query definitions and result transformations.
3. Shared filter state, compatibility rules, reset, and stale-request cancellation.
4. KPI and trend views.
5. Investment, initiative, asset visibility, and AI detection views.
6. Loading, empty, partial-error, retry, and no-selection states.
7. Keyboard/accessibility behavior and responsive layout.
8. Automated tests and Playwright browser scenarios.

After each phase, inspect the changed queries against the TMDL. Measure names containing spaces or punctuation must be referenced exactly as required by the starter's query API.

## Exercise 5: Preview in the Fabric shell

Start the local frontend:

```powershell
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

## Exercise 6: Run automated validation

Run the starter's checks:

```powershell
npm run lint
npm run test
npm run build
```

Run the project's Playwright command if Copilot added one, typically:

```powershell
npm run test:e2e
```

The browser suite should cover:

- Nonblank initial render after loading.
- A filter selection changing at least two compatible visuals.
- Reset restoring default query state.
- Empty and failed-query messages.
- Keyboard access to filters and reset.
- Desktop and mobile viewports with no overlapping text or controls.

Inspect screenshots rather than treating a successful element lookup as visual proof.

{: .checkpoint }
Lint, unit/component tests, production build, and browser checks pass; desktop and mobile screenshots show a usable, nonblank dashboard.

## Exercise 7: Deploy the Fabric App

Use the starter's documented Rayfin/Fabric deployment command. Confirm the environment points to the deployed Contoso model, then deploy to the same capacity-backed workspace.

After deployment:

1. Open the App URL and verify Microsoft Entra ID SSO.
2. Confirm the deployed app queries the intended semantic model ID.
3. Repeat one cross-filter and reset scenario.
4. Test with a user who has **Run and interact** on the app and **Build** permission on the semantic model.
5. Confirm no token or credential appears in source, generated JavaScript, browser storage, or network query parameters.

## Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Helper returns `401` | Run `az login` again. The helper requests the `https://api.fabric.microsoft.com` audience. |
| Helper returns `403` | Stop and obtain Contributor or higher workspace access. |
| Helper reports no capacity | Assign the workspace to a supported Fabric capacity before retrying. |
| A query reports an unknown field or measure | Compare its exact name and table with the local TMDL; do not guess aliases. |
| Local page is blank outside Fabric | Use the Fabric shell URL with `devUri` so brokered authentication/context is available. |
| Filters race and show stale results | Cancel or disregard older requests when filter state changes. Add a regression test. |

## Clean up

Delete the deployed Fabric App when finished. Delete **Contoso DT Dashboard** only if it was created specifically for this lab and is not used by another app or report.

## Completion criteria

- The bundled TMDL model is reproducibly deployed and its ID recorded.
- The approved plan maps every visual to real model metadata.
- Compatible visuals cross-filter through shared state and reset correctly.
- Robust states, keyboard access, and responsive layouts are validated.
- All automated checks pass and the app works through Fabric SSO.

[Previous: Lab 2]({% link labs/lab-2-field-technician.md %}){: .btn }
[Back to labs]({% link labs/index.md %}){: .btn .btn-primary }
