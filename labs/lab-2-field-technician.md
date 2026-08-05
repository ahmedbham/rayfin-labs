---
layout: default
title: "Lab 2: Field technician app"
parent: Labs
nav_order: 2
description: Use GitHub Copilot Plan mode and Code mode to build a role-aware field service Fabric App.
---

# Lab 2: Build a field technician app

**Estimated time:** 90-150 minutes

In this lab, GitHub Copilot helps you turn business requirements into an implementation plan and then into a full-stack Fabric App. Rayfin generates the data API and provisions a SQL database in Fabric from TypeScript entities.

## Objectives

- Produce and review a requirements-traceable implementation plan.
- Design role-aware entities and authorization for dispatchers and technicians.
- Implement operational workflows with generated Rayfin APIs and storage.
- Validate locally and deploy the completed application to Fabric.

## Before you begin

Complete the [prerequisites]({% link prerequisites.md %}) and [Lab 1]({% link labs/lab-1-todo.md %}). Keep this workshop open in one VS Code window and create the learner app in a separate folder or window.

Open these authoritative inputs before planning:

- [Lab 2 prompt](https://github.com/ahmedbham/rayfin-labs/blob/main/LAB_2_PROMPT.md)
- [Field technician functional requirements](https://github.com/ahmedbham/rayfin-labs/blob/main/LAB_2_FUNCTIONAL_REQUIREMENTS.md)

{: .important }
Copilot can accelerate implementation, but you own the schema and authorization design. Never approve a plan that relies only on hidden UI controls to enforce dispatcher or technician permissions.

## Exercise 1: Create a Rayfin project

In a projects folder, scaffold a current Rayfin starter suitable for a data-driven React application:

```powershell
npm create @microsoft/rayfin@latest
```

Name it `field-technician-app`, select a TypeScript/React template with data and authentication, then install dependencies and open it:

```powershell
cd field-technician-app
npm install
code .
```

Copy `LAB_2_PROMPT.md` and `LAB_2_FUNCTIONAL_REQUIREMENTS.md` from this workshop into a temporary `requirements/` folder in the generated project. These files are design inputs; do not place them in the production frontend bundle.

Inspect the scaffold's `AGENTS.md`, `.agents/skills/`, Rayfin configuration, data entities, package scripts, and existing tests. Current templates can differ, so these local instructions take precedence over assumed paths.

## Exercise 2: Generate the implementation plan

Open Copilot Chat and select **Plan** mode. Attach both files from `requirements/`, then enter:

> Follow `LAB_2_PROMPT.md`. Analyze `LAB_2_FUNCTIONAL_REQUIREMENTS.md` and this scaffolded Rayfin project. Produce a detailed, ordered implementation plan. Do not edit files. Include a traceability matrix from requirement sections 3-12 to plan steps, identify authorization boundaries, state assumptions, and list focused validation after each implementation phase.

Save the proposed plan in the location offered by Copilot or in `IMPLEMENTATION_PLAN.md`.

### Review rubric

Do not switch modes until the plan covers all of the following:

| Area | The plan must address |
|:-----|:----------------------|
| Identity | Profile setup, role selection, assigned regions, first-login routing, and clear setup failures. |
| Data model | Profiles, regions and membership, customers, jobs, assignments, checklist items, equipment, notes/history, help requests, and image metadata. |
| Authorization | Server-enforced authenticated access plus dispatcher/technician ownership and region rules. |
| Dispatcher | Attention queues, customer search/create, job creation/assignment, job detail updates, and default region. |
| Technician | Scheduled, unscheduled, and finished queues; status/on-site/checklist/equipment/note updates; help requests. |
| Files | One image per new note, preview/removal, storage reference, camera fallback, and failed-save behavior. |
| Reliability | Loading, empty, validation, success, not-found, and error states; manual and 30-second refresh. |
| Delivery | Sample data, unit/component tests, representative browser workflows, lint, build, migration, and Fabric deployment. |

Ask Copilot to revise omissions. Challenge these common weak assumptions:

- A user-selected role is automatically trustworthy for authorization.
- Region membership can be represented by a single string when requirements allow assignment to at least one region.
- Photos can safely be stored as base64 text in the database or frontend.
- Polling can start repeatedly without cancellation when routes change.
- Sample data can depend on fixed user IDs that will not exist after deployment.

{: .checkpoint }
The approved plan maps every requirements section to implementation and validation steps, with explicit authorization policies and no unresolved blocking assumptions.

## Exercise 3: Implement the data foundation

Switch Copilot Chat to **Agent** mode. In this lab, Agent mode is the Code mode that implements the approved plan. Enter:

> Implement the approved plan one phase at a time. Start only with the Rayfin entities, relationships, authorization policies, schema export, and sample-data strategy. Preserve scaffold conventions. After editing, run the narrowest schema, type, or test validation available and stop for my review.

Review every entity before accepting it:

1. IDs, foreign keys, optional fields, and timestamps match the workflows.
2. Status and role values cannot drift through arbitrary strings.
3. Customer phone search has an appropriate normalized/searchable representation.
4. Jobs can be unassigned and unscheduled without invalid placeholder values.
5. Note image records reference managed storage rather than exposing secrets.
6. Authorization policies constrain records on the backend.

Start the local backend, apply migrations with the scripts generated by the template, and load sample data. Typical experimental-template commands are:

```powershell
npm run dev:local
npm run rayfin:db
```

Use the actual scripts in `package.json` if they differ.

{: .checkpoint }
The local schema applies successfully and sample data includes at least two regions, a dispatcher, two technicians, customers, scheduled and unscheduled jobs, an overdue job, active work, completed work, and a help request.

## Exercise 4: Implement application workflows

Continue in Agent mode phase by phase. After each phase, ask Copilot to run focused tests and summarize changed files.

Recommended order:

1. Authentication gate and first-time profile setup.
2. Shared job summaries and job detail loading.
3. Dispatcher home, customer search/create, and job creation.
4. Technician queues and job updates.
5. Help request, checklist, equipment, and history interactions.
6. Image selection, preview, camera fallback, upload, and note save.
7. Polling, manual refresh, error boundaries, accessibility, and responsive layout.
8. Sample-data page and final navigation.

For each phase, inspect the browser rather than relying only on tests. Confirm buttons cannot be submitted repeatedly, fields identify validation errors, and empty/error messages explain what the user can do next.

## Exercise 5: Validate both roles

Run all project checks:

```powershell
npm run lint
npm run test
npm run build
```

Then complete these browser scenarios using separate local accounts or sessions:

### Dispatcher scenario

1. Complete profile setup and create a new region.
2. Search for a customer by phone, create one, then create a scheduled assigned job.
3. Create an unscheduled unassigned job.
4. Confirm overdue, unscheduled, active, and help-request sections classify sample jobs correctly.
5. Open the technician's help request and read its explanation.

### Technician scenario

1. Complete profile setup in an existing region.
2. Confirm scheduled, unscheduled, and finished queues are correctly ordered.
3. Open an assigned job, mark on-site, update status, checklist, and equipment.
4. Add a text note, then add a note with an image preview.
5. Request dispatcher help and confirm the indicator appears after refresh.

Wait at least 30 seconds on a dashboard and confirm automatic refresh does not duplicate content or lose the current route. Denied operations should return an authorization error even when attempted outside the visible UI.

{: .checkpoint }
All automated checks pass and both role scenarios satisfy the functional requirements, including failure and empty states.

## Exercise 6: Deploy to Fabric

Run the scaffold's deployment command, typically:

```powershell
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

[Previous: Lab 1]({% link labs/lab-1-todo.md %}){: .btn }
[Next: Lab 3]({% link labs/lab-3-dashboard.md %}){: .btn .btn-primary }
