---
layout: default
title: "Lab 1: Todo app"
parent: Labs
nav_order: 1
description: Scaffold, run, inspect, modify, test, and deploy a basic Fabric App with Rayfin CLI.
---

# Lab 1: Build a Todo app

**Estimated time:** 45-60 minutes

In this lab, you use the experimental full-local Todo template to follow a Fabric App through its complete lifecycle. The application supports sign-up, sign-in, and per-user Todo create, read, update, and delete operations.

## Objectives

By the end of this lab, you can:

- Scaffold a Rayfin project from a community template.
- Run authentication, data, and hosting services locally with Docker.
- Relate a TypeScript entity to the generated data API and typed client.
- Validate and deploy the application to Microsoft Fabric.

## Before you begin

Complete the [prerequisites]({% link prerequisites.md %}), including a capacity-backed Fabric workspace.

{: .warning }
The template uses experimental username/password authentication and Docker local hosting. Its APIs and commands can change. Deployed Fabric Apps use Microsoft Entra ID single sign-on instead of local password authentication.

## Choose your environment

Running this lab on a laptop is recommended. From the cloned repository root, authenticate Azure CLI and Rayfin with the same Microsoft Entra tenant account:

```bash
az login -t <tenant-id>
rayfin login -t <tenant-id>
```

If the generated template specifically requires `rayfin auth` and `rayfin help` lists it, run that command as well.

GitHub Codespaces is also supported. Open a Codespace from your fork, verify Azure CLI is installed, and run `rayfin login -t <tenant-id> --encryption-fallback-enabled`. If its browser callback shows **Hmmm... can't reach this page**, copy the complete `localhost:` callback URL and run it from a second Codespaces terminal:

```bash
curl "<copied-url>"
```

### Exercise 1: Scaffold the application

Open a terminal at the root of this cloned workshop repository. 

```bash
mkdir rayfin-todo-app && cd rayfin-todo-app
rayfin init --template https://github.com/microsoft/awesome-rayfin --template-name "[Experimental] Todo app with full local dev"
```

When prompted, name the project `rayfin-todo-app`. Then open it in VS Code:

```bash
npm install
```

### Inspect the generated project

Before running the app, find these files in Explorer:

| Surface | Typical location | Responsibility |
|:--------|:-----------------|:---------------|
| Service configuration | `rayfin/rayfin.yml` | Authentication and local/deployed services. |
| Todo entity | `rayfin/data/Todo.ts` | Database fields, validation, and per-user authorization. |
| Schema export | `rayfin/data/schema.ts` | Entities exposed through the generated data API. |
| Client bootstrap | `src/services/bootstrap.ts` | Selects local password or Fabric brokered authentication. |
| Todo operations | `src/services/todos.ts` | Type-safe queries and mutations. |
| Main page | `src/pages/HomePage.tsx` | Todo interaction and UI states. |

In `Todo.ts`, locate the `@entity()` decorator and the `@role()` policy. Trace how the policy compares the signed-in subject claim with each Todo's user ID.

{: .checkpoint }
You can explain which file defines storage and authorization, and which file calls that generated API from the browser.

### Exercise 2: Run the full stack locally

Start Docker Desktop and verify the engine:

```bash
docker info
```

In the VS Code terminal, start the backend containers and Vite:

```bash
npm run dev:local
```

Keep that terminal running. The public Rayfin webservice image is pulled automatically the first time, which can take several minutes.

Open a second terminal and apply the database migration:

```bash
npm run rayfin:db
```

Open [http://localhost:5173](http://localhost:5173). Create an account with a test email and password, then:

1. Create three Todos.
2. Mark one Todo complete.
3. Delete another Todo.
4. Refresh the browser and confirm the remaining data persists.
5. Sign out, create a second account, and confirm it cannot see the first account's Todos.

{: .checkpoint }
Local authentication works, CRUD changes survive refresh, and the role policy isolates data between users.

### Exercise 3: Validate the project

Run the checks exposed by the template:

```bash
npm run lint
npm run test
npm run build
```

Fix issues introduced by your UI change. Do not disable a lint rule or remove a test merely to make a check pass.

To inspect local service status or reset the environment, use:

```bash
npm run rayfin:dev -- status
npm run dev:local:stop
npm run dev:local:down
```

Use `npm run dev:local:purge` only when you intentionally want to delete local volumes and all Todo data.

{: .checkpoint }
Lint, tests, and the production build complete successfully.

### Exercise 4: Deploy to Fabric

Stop the local development command. Sign in when the Rayfin CLI prompts you, then run:

```bash
npm run up
```
After deployment:

1. Open the Fabric workspace and select the new Fabric App.
2. Open the **App URL** and confirm Microsoft Entra ID SSO signs you in.
3. Create and update a Todo in the deployed app.
4. Return to the Fabric item and inspect its child **SQL database in Fabric**.
5. Confirm that another tester has **Run and interact** permission before asking them to open the app.

Do not change the generated schema directly in the Fabric SQL editor. Schema changes belong in the TypeScript entity and are applied through Rayfin.

{: .checkpoint }
The deployed URL loads with Fabric SSO, Todo operations succeed, and the generated SQL database appears as a child item.

**IMPORTANT**: Open .env file under rayfin folder for Todo app and capture the value for RAYFIN_PUBLIC_WORKSPACE_ID. This ID represents the Workspace ID for `My workspace` and needs to be specified in the prompt for Lab 2 and Lab 3 if you are using this workspace for these labs.

### Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Docker image pull is stale or fails | Run `docker pull ghcr.io/microsoft/rayfin/webservice:latest`, then retry. |
| A Rayfin command reports that authentication is required | Run `rayfin login -t <tenant-id>`; add `--encryption-fallback-enabled` in Codespaces. If the project explicitly requires `rayfin auth` and `rayfin help` lists it, run that too. |
| App loads but data operations fail locally | Confirm `npm run rayfin:db` completed after the containers started. |
| Port 5173 is already used | Stop the other Vite process or use the alternate URL Vite prints. |
| Local login works but deployed login differs | This is expected: deployment uses Fabric brokered Microsoft Entra ID authentication. |
| Deployment cannot create items | Confirm the workspace has capacity and you have Contributor or higher access. |

## Clean up

Stop local services without deleting data:

```bash
npm run dev:local:stop
```

When the deployed resources are no longer needed, delete the parent Fabric App from the workspace and confirm its child items are removed.

## Completion criteria

- Local CRUD and user isolation are demonstrated.
- The customized project passes lint, tests, and build.
- The app is deployed and validated with Fabric SSO.
- You can identify the entity, authorization policy, typed client, and UI surfaces.

[Next: Lab 2]({% link labs/lab-2-dashboard.md %}){: .btn .btn-primary }
