# Agent Conventions

## Purpose

This file guides coding agents working in this repository. Keep it operational and project-specific. Use `README.md` for package usage and `docs/developer.md` for local setup details; do not duplicate those walkthroughs here.

## Workflow Tools

- Use `uv` for contributor and agent workflows by default.
- Use `uv sync` to create or refresh the local environment.
- Use `uv run ...` for project commands instead of bare `python`, `pip`, or globally installed tooling unless the task explicitly requires it.
- Use Ruff for Python formatting and linting by default.

## Repo Map

- `wagtail_honeypot/`: package behavior and public implementation.
- `wagtail_honeypot/models.py`: honeypot settings defaults and form submission logic.
- `wagtail_honeypot/templatetags/honeypot_tags.py`: template tag context and field names.
- `wagtail_honeypot/templates/` and `wagtail_honeypot/static/`: rendered markup and browser-side behavior.
- `wagtail_honeypot/locale/`: translations.
- `tests/`: unit coverage for models, methods, forms, and template tags.
- `tests/testapp/`: minimal Wagtail integration site; use it only when a change needs page-level or form-flow coverage.

## Change Conventions

- Put reusable package behavior in `wagtail_honeypot/`, not in `tests/testapp/`.
- Change `models.py` when adjusting honeypot defaults, settings handling, or form submission decisions.
- Change `templatetags/honeypot_tags.py` and `templates/tags/honeypot_fields.html` when adjusting rendered field names, context, or markup.
- Change `static/css/` or `static/js/` only for browser behavior related to hiding or presenting honeypot fields.
- Update `locale/` only when user-facing strings change.
- Keep `tests/testapp/` focused on integration behavior; do not treat it as a second implementation surface.

## Compatibility Rules

- Preserve existing `HONEYPOT_*` setting names and behavior unless the task explicitly changes support policy.
- Avoid unnecessary breaking changes to template tag output, rendered field attributes, or form-processing semantics.
- Treat the Django and Wagtail support matrix in `tox.ini` as a constraint when making changes.
- Preserve backwards compatibility across supported versions unless the task explicitly requires otherwise.

## Testing Expectations

- For model or method changes, add or update focused tests in `tests/test_models.py` or `tests/test_methods.py`.
- For form submission behavior, update `tests/test_form.py` and verify both accepted and ignored submissions.
- For template tag or rendered field changes, update `tests/test_tags.py` with context and rendered HTML assertions.
- Use `tests/testapp/` coverage when the change affects Wagtail page behavior or end-to-end form flow.
- For translation or configuration changes, add focused assertions where practical.
- Run `make lint` or `uv run ruff check .` for Python style checks.
- Run `make format` or `uv run ruff format .` when updating Python formatting.
- Run `make test` or `uv run coverage run manage.py test` for the default suite.
- Use `make tox` or `uv run tox --skip-missing-interpreters` only when matrix coverage is relevant to the task.

## Documentation Rules

- Update `README.md` when package usage, settings, or integration steps change for users.
- Update `docs/developer.md` when local development workflow changes.
- Update `CHANGELOG` under `## Unreleased` for every PR. Keep entries short, flat, and user or contributor facing.
- Keep `AGENTS.md` concise and directive; do not turn it into a duplicate contributor guide.

## PR Readiness

- Keep the pull request title and body aligned with the current branch scope.
- Update the PR title whenever the branch scope changes materially and the current title no longer describes the work accurately.
- Update the PR description whenever behavior, tooling, documentation, or test coverage changes materially from the current summary.
- The maintained PR body should cover the behavior change, docs or tooling updates, and verification performed.
- Treat the PR title, PR summary, and `CHANGELOG` entry as required closing steps before the branch is ready.

## Branch Workflow

- Treat `release` as the repository default branch.
- Start all new work from `release`; it tracks the latest changes that are not yet released to PyPI.
- Treat `main` as the release-preparation branch, not the starting point for routine feature or fix work.
- Target merge requests at `release`.

## Change Boundaries

- Do not change version metadata, supported-version claims, or migrations unless the task requires it.
- Keep commit scope narrow and tied to one behavior change.
- Prefer minimal edits that preserve the package's existing API and documented behavior.
