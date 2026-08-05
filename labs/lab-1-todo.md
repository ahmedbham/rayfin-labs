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

Complete the [prerequisites]({% link prerequisites.md %}), including Docker Desktop and a capacity-backed Fabric workspace.

{: .warning }
The template uses experimental username/password authentication and Docker local hosting. Its APIs and commands can change. Deployed Fabric Apps use Microsoft Entra ID single sign-on instead of local password authentication.

## Exercise 1: Scaffold the application

Open PowerShell in a folder where you keep projects. Do not generate the application inside the cloned workshop repository.

```powershell
npm create @microsoft/rayfin@latest -- --template https://github.com/microsoft/awesome-rayfin --template-name "[Experimental] Todo app with full local dev"
```

When prompted, name the project `rayfin-todo-app`. Then open it in VS Code:

```powershell
cd rayfin-todo-app
code .
npm install
```

If the scaffold command reports that the template name is unavailable, open the [current Todo template](https://github.com/microsoft/awesome-rayfin/tree/main/templates/todo-local-experimental), copy its displayed install command, and use the current name.

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

## Exercise 2: Run the full stack locally

Start Docker Desktop and verify the engine:

```powershell
docker info
```

In the VS Code terminal, start the backend containers and Vite:

```powershell
npm run dev:local
```

Keep that terminal running. The public Rayfin webservice image is pulled automatically the first time, which can take several minutes.

Open a second terminal and apply the database migration:

```powershell
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

## Exercise 3: Make a small change

Change the application title and empty-state message in the relevant React components. Use a name and message that make the app recognizably yours.

Save the files and observe Vite update the browser without restarting the backend. Check the page at narrow and wide browser widths and verify that controls remain usable.

Next, ask Copilot Chat this focused question without asking it to edit code:

> Trace a Todo from the form submission through the typed Rayfin client to the entity definition. Identify the files and methods involved, and explain where authorization is enforced.

Compare its answer with the files you inspected. Treat Copilot's explanation as a hypothesis and verify every reference in the code.

## Exercise 4: Validate the project

Run the checks exposed by the template:

```powershell
npm run lint
npm run test
npm run build
```

Fix issues introduced by your UI change. Do not disable a lint rule or remove a test merely to make a check pass.

To inspect local service status or reset the environment, use:

```powershell
npm run rayfin:dev -- status
npm run dev:local:stop
npm run dev:local:down
```

Use `npm run dev:local:purge` only when you intentionally want to delete local volumes and all Todo data.

{: .checkpoint }
Lint, tests, and the production build complete successfully.

## Exercise 5: Deploy to Fabric

Stop the local development command. Sign in when the Rayfin CLI prompts you, then run:

```powershell
npm run up
```

Select the capacity-backed workspace prepared earlier. If the generated template exposes `npm run dev` as its cloud-connected development command, you can use it to deploy services and run Vite locally against the Fabric backend:

```powershell
npm run dev
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

## Troubleshooting

| Symptom | Resolution |
|:--------|:-----------|
| Docker image pull is stale or fails | Run `docker pull ghcr.io/microsoft/rayfin/webservice:latest`, then retry. |
| App loads but data operations fail locally | Confirm `npm run rayfin:db` completed after the containers started. |
| Port 5173 is already used | Stop the other Vite process or use the alternate URL Vite prints. |
| Local login works but deployed login differs | This is expected: deployment uses Fabric brokered Microsoft Entra ID authentication. |
| Deployment cannot create items | Confirm the workspace has capacity and you have Contributor or higher access. |

## Clean up

Stop local services without deleting data:

```powershell
npm run dev:local:stop
```

When the deployed resources are no longer needed, delete the parent Fabric App from the workspace and confirm its child items are removed.

## Completion criteria

- Local CRUD and user isolation are demonstrated.
- The customized project passes lint, tests, and build.
- The app is deployed and validated with Fabric SSO.
- You can identify the entity, authorization policy, typed client, and UI surfaces.

[Next: Lab 2]({% link labs/lab-2-field-technician.md %}){: .btn .btn-primary }
