# Lab 2 implementation prompt

Build a Microsoft Fabric App using Rayfin CLI that implements the functional requirements in `LAB_2_FUNCTIONAL_REQUIREMENTS.md`.

Use Rayfin TypeScript entities to provision the application's SQL database in Fabric and generated data API. Implement role-aware authorization for dispatcher and technician workflows. Use Rayfin storage for job-note images when supported by the selected template.

Before writing code:

1. Inspect the functional requirements and the scaffolded Rayfin project.
2. Research the Rayfin patterns already available in the project and its installed skill or agent instructions.
3. Produce an implementation plan covering the data model, authorization, routes, services, UI states, sample data, tests, and deployment.
4. Map each functional-requirements section to one or more plan steps and identify assumptions or unsupported capabilities.

During implementation, keep credentials and tokens out of source code and frontend assets. Add loading, empty, validation, success, and error states. Validate the result with lint, automated tests, a production build, and representative dispatcher and technician workflows.
