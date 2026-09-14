---
layout: default
title: "Lab 3: Field technician app"
parent: Labs
nav_order: 3
description: Use GitHub Copilot Plan mode and Code mode to build a role-aware field service Fabric App.
redirect_from:
  - /labs/lab-2-field-technician.html
---

# Lab 3: Build a field technician app

**Estimated time:** 90-150 minutes

In this lab, GitHub Copilot helps you turn business requirements into an implementation plan and then into a full-stack Fabric App. Rayfin generates the data API and provisions a SQL database in Fabric from TypeScript entities.

## Objectives

- Produce and review a requirements-traceable implementation plan.
- Design role-aware entities and authorization for dispatchers and technicians.
- Implement operational workflows with generated Rayfin APIs and storage.
- Validate locally and deploy the completed application to Fabric.

## Before you begin

Complete the [prerequisites]({% link prerequisites.md %}), [Lab 1]({% link labs/lab-1-todo.md %}), and [Lab 2]({% link labs/lab-2-dashboard.md %}). Running the lab on a laptop is recommended, and GitHub Codespaces is also supported. Keep this workshop open while you work in the generated app folder inside the repository.

From the repository root on a laptop, run `az login -t <tenant-id>` and then `rayfin login -t <tenant-id>`. In Codespaces, add `--encryption-fallback-enabled` to the Rayfin login and use the callback workaround from the prerequisites if the browser cannot reach `localhost`. If the generated template specifically requires `rayfin auth` and `rayfin help` lists it, run that command as well.

Open these authoritative inputs before planning:

- [Lab 3 prompt](https://github.com/ahmedbham/rayfin-labs/blob/main/lab-assets/lab-3/LAB_3_PROMPT.md)
- [Field technician functional requirements](https://github.com/ahmedbham/rayfin-labs/blob/main/lab-assets/lab-3/LAB_3_FUNCTIONAL_REQUIREMENTS.md)

## Exercise 1: Create a Rayfin project

From this workshop repository root, scaffold a current Rayfin starter suitable for a data-driven React application. `rayfin init` creates the project folder; do not create or switch to another parent folder first.

```bash
mkdir field-technician-app && cd field-technician-app
rayfin init
```

- In response to `How would you like to start?`, select **Use a template (built-in)**.
- Under `Select a template:`, select `1` (**Blank App - Bare-bones Fabric-authenticated React + Vite app — sign-in, routing, and a placeholder home page, with no data layer to remove**)
- Under `Project name:`, enter `field-technician-app`.

```bash
cd field-technician-app
npm install
```

## Exercise 2: Generate the implementation plan

Open Copilot Chat and select **Agent** mode. Attach folder `lab-assets/lab-3/` folder, then enter:

> Follow `LAB_3_PROMPT.md`. 


## Exercise 6: Deploy to Fabric

Run the scaffold's deployment command, typically:

```bash
npm run up
```

Select the capacity-backed workspace. After deployment:

1. Open the App URL and complete a new SSO-backed profile.
2. Repeat one dispatcher and one technician workflow with deployed identities.
3. Inspect the generated child SQL database in Fabric and confirm expected tables exist.
4. Verify uploaded images render through the deployed storage path and are not public secrets embedded in HTML.
5. Grant a tester **Run and interact** permission and confirm they cannot perform operations outside their role.

Schema changes must continue to originate in the Rayfin TypeScript model, not through direct edits in the SQL database portal.

## Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Copilot starts editing in Plan mode | Stop the response, restore unintended edits, and repeat the prompt with “Do not edit files.” |
| Migration fails after an entity change | Read the generated migration/schema error, verify relationship types and optional fields, then use the template's supported reset only if local data can be deleted. |
| A technician sees unrelated jobs | Treat this as an authorization defect, not a filtering bug. Fix the backend role policy and add a regression test. |
| Camera access is denied | Show the expected explanation and validate file selection as the fallback. Camera support requires browser/device permission and usually a secure context. |
| Polling causes repeated requests after navigation | Ensure the interval is created once and canceled when the page unmounts or authentication changes. |

## Clean up

Stop or remove local containers using the scaffold's scripts. Delete the deployed parent Fabric App when it is no longer needed and verify its child database and storage items are removed.

## Completion criteria

- An approved plan traces all functional requirements.
- Backend authorization protects dispatcher and technician operations.
- Both role workflows, image notes, polling, sample data, and error states work locally.
- Lint, tests, and production build pass.
- The deployed app works with Fabric SSO and its generated SQL database.

[Previous: Lab 2]({% link labs/lab-2-dashboard.md %}){: .btn }
[Back to labs]({% link labs/index.md %}){: .btn .btn-primary }
