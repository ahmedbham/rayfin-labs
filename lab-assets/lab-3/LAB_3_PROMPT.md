# Lab 3 implementation prompt

Implement the field technician application in `field-technician-app`.

Treat `lab-assets/lab-3/LAB_3_FUNCTIONAL_REQUIREMENTS.md` as authoritative.
This is a technician-only application. Exclude dispatcher dashboards,
customer CRUD, job creation, scheduling, and technician assignment except
for owner-scoped sample records.

Use the project-local Rayfin CLI and version-locked documentation. Do not
assume the globally installed CLI has the same commands or syntax.

Implementation decisions:

- Profiles have exactly one service region.
- Backend authorization must restrict every technician-owned record using
  `claims.sub`; frontend filtering is not a security boundary.
- The sample-data page is available in local and deployed environments,
  is scoped to the signed-in user, and must be idempotent.
- Operational jobs come from the separate dispatcher application. The
  technician app may create only records marked as sample data.
- Build a mobile-first, accessible React interface.
- Use the existing authentication and scaffold conventions.

Implement end to end without stopping for phase reviews. Add focused tests,
then run lint, tests, build, Rayfin schema validation or dry run, and start
the local app. Do not deploy unless explicitly requested.

Report unmet requirements, if any, and include the reason.