# Releasing wagtail-honeypot

This is the maintainer runbook for publishing package releases to PyPI via GitHub Actions.

## Release Workflow

- Workflow file: `.github/workflows/release.yml`
- Trigger: GitHub Release event `published`
- Authentication: PyPI Trusted Publisher (OIDC), no API token secret

The release workflow:

1. validates GitHub release tag (`vX.Y.Z` or pre-release like `vX.Y.Zrc1`) matches `project.version` in `pyproject.toml`
2. validates the tagged commit is contained in `origin/main`
3. builds `sdist` + `wheel` with `uv build`
4. runs `twine check` on built artifacts
5. publishes artifacts to PyPI using `pypa/gh-action-pypi-publish`

## One-Time Setup (PyPI Trusted Publisher)

In the PyPI project settings for `wagtail-honeypot`, add a Trusted Publisher with:

- Owner or organization: `nm-packages`
- Repository: `wagtail-honeypot`
- Workflow: `release.yml`
- Environment: unset (unless intentionally adding GitHub Environments later)

The GitHub repository and workflow identity must match exactly, or publish will fail.

## Maintainer Release Steps

1. Keep `CHANGELOG` updated under `## Unreleased` for every merged PR landing on `main`.
2. Update `version` in `pyproject.toml` to the intended release version.
3. Convert the current `## Unreleased` notes in `CHANGELOG` into the new release entry, then leave a fresh `## Unreleased` placeholder for future work.
4. Review user-facing docs and examples that intentionally describe the current release, and either:
   - update them to the new version where exact release numbers are still useful, or
   - remove brittle hardcoded release numbers when the docs work just as well without them.
5. Merge the release-prep changes to `main`.
6. Ensure normal CI on `main` is green (`Tests` workflow).
7. Create a GitHub Release with a tag that matches the package version with `v` prefix.
8. Use the `CHANGELOG` entry as the GitHub Release body.
9. Publish the GitHub Release.
10. Confirm `.github/workflows/release.yml` succeeds and the version appears on PyPI.

For local sandbox/test command workflows before a release, use:

- [developer.md](../developer.md) for canonical developer workflow and quickstart commands
- [AGENTS.md](https://github.com/nm-packages/wagtail-honeypot/blob/main/AGENTS.md) for canonical contributor command/reference guidance

## Changelog Maintenance

- Add or update a `CHANGELOG` entry under `## Unreleased` in every PR.
- During release prep, move or rewrite the `Unreleased` notes into the new versioned release section.
- After release prep, keep an empty `## Unreleased` section in place for subsequent work.
- During release prep, review any docs/examples that intentionally point at the current package release and avoid leaving stale version numbers in user-facing pages.

Examples:

- `pyproject.toml` version `1.3.0` => GitHub tag `v1.3.0`, release title `1.3.0` (or `Release 1.3.0`)
- `pyproject.toml` version `1.4.0rc1` => GitHub tag `v1.4.0rc1`, release title `1.4.0rc1` (or `Release 1.4.0rc1`)

## Local Preflight (Optional but Recommended)

Run these before creating the GitHub Release:

```bash
uv build --sdist --wheel --out-dir /tmp/wagtail-honeypot-dist-check
uvx twine check /tmp/wagtail-honeypot-dist-check/*
```

## Failure Modes and Troubleshooting

- Tag/version mismatch:
  - Symptom: workflow fails in "Validate release tag matches package version"
  - Fix: align GitHub tag with `pyproject.toml` version and republish release
- Tag commit not on main:
  - Symptom: workflow fails in "Validate release commit is on main"
  - Fix: retag a commit that is on `main`
- Trusted Publisher identity mismatch:
  - Symptom: PyPI publish step reports authorization/trust failure
  - Fix: verify owner/repo/workflow values in PyPI Trusted Publisher settings
- Duplicate version:
  - Symptom: publish step fails because version already exists on PyPI
  - Fix: bump `pyproject.toml` version and publish a new tag/release
