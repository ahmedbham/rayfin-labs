# Build Fabric Apps with Rayfin

Hands-on labs for building Microsoft Fabric Apps with Rayfin CLI and GitHub Copilot.

The published workshop uses Jekyll and the Just the Docs theme. Its three labs cover a guided Todo app, a requirements-driven field technician app, and an interactive dashboard over a Power BI semantic model.

## Source artifacts

- `LAB_2_PROMPT.md` and `LAB_2_FUNCTIONAL_REQUIREMENTS.md` drive the Lab 2 Copilot workflow.
- `LAB_3_PROMPT.md` drives the Lab 3 Copilot workflow.
- `Contoso-DT-Dashboard.SemanticModel/` contains the Lab 3 TMDL semantic model.
- `scripts/deploy_semantic_model.py` packages and deploys that model through the Fabric REST API.

## Preview the documentation

Ruby 3.3 and Bundler are required for a local preview.

```powershell
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000/rayfin-labs/`.

Alternatively, use Docker from the repository root:

```powershell
docker run --rm -p 4000:4000 -v "${PWD}:/srv/jekyll" -w /srv/jekyll ruby:3.3-bookworm bash -lc "bundle install; bundle exec jekyll serve --host 0.0.0.0"
```

## Publish

The workflow in `.github/workflows/pages.yml` builds and deploys the `main` branch. In the repository settings, set **Pages > Build and deployment > Source** to **GitHub Actions**.

Fabric Apps and full local Rayfin development are preview or experimental experiences. Review upstream documentation if generated commands differ from the lab text.
