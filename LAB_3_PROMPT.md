# Lab 3 implementation prompt

Build a [Microsoft Fabric App](https://learn.microsoft.com/fabric/apps/overview) using [Rayfin CLI](https://github.com/microsoft/rayfin) as an interactive, cross-filterable interface to the Power BI semantic model in the `Contoso-DT-Dashboard.SemanticModel` folder. Use [rayfin-nyc-taxi-app](https://github.com/ahmedbham/rayfin-nyc-taxi-app) as the code-sample template and preserve its Fabric authentication and semantic-model query patterns.

Before writing code, inspect the semantic model's tables, measures, columns, and relationships and produce an implementation plan that maps every proposed visual to real model fields or measures. Include KPI summaries and analytical views for operational metrics, investment, initiatives, asset visibility, and AI detections.

Selections in filters and visuals must update all compatible visuals through shared filter state. Include a clear reset action and robust loading, empty, partial-data, and error states. The interface must be keyboard accessible and responsive on desktop and mobile.

Do not hard-code access tokens, tenant IDs, credentials, or environment-specific semantic model IDs in committed source. Use the template's environment/configuration pattern. Validate the implementation with lint, tests, a production build, and automated browser checks for initial rendering, cross-filtering, reset behavior, error states, and desktop/mobile layout.
