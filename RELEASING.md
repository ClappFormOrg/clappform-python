# Releasing

Publishing to PyPI is human-gated and uses **Trusted Publishing (OIDC)** — no
API tokens are stored in the repo. The `Release` workflow (`.github/workflows/release.yml`)
builds and verifies the distributions, then waits on the protected `pypi`
environment's required-reviewer approval before uploading.

## One-time setup

1. **PyPI trusted publisher.** On the `clappform` project at
   <https://pypi.org/manage/project/clappform/settings/publishing/>, add a
   GitHub Actions trusted publisher:
   - Owner: `ClappFormOrg`
   - Repository: `clappform-python`
   - Workflow: `release.yml`
   - Environment: `pypi`
2. **GitHub environment.** In the repository settings → Environments, create an
   environment named `pypi` and add the release maintainers as **required
   reviewers**. This is the approval gate the publish job pauses on.

## Cutting a release

1. Land everything for the release on `Major/6`, then promote to the default
   branch per the branch flow.
2. Bump `version` in `pyproject.toml` (pre-releases use PEP 440 suffixes, e.g.
   `6.0.0a1`, `6.0.0rc1`). Commit.
3. Tag and publish a **GitHub Release** whose tag matches the version
   (`v6.0.0a1` or `6.0.0a1`). Put the release notes — including the proto diff
   of the sync — in the release body.
4. The `Release` workflow runs: it builds the sdist + wheel, fails if the tag
   and packaged version disagree, and validates metadata with `twine check`.
5. The `publish` job then pauses on the `pypi` environment. A required reviewer
   approves, and only then does the upload run.

Pre-releases (`aN`/`bN`/`rcN`) are not installed by a plain `pip install
clappform`; users opt in with `pip install --pre clappform` or a pinned
`clappform==6.0.0a1`.

## Verifying locally before you tag

```bash
make release-check   # build sdist+wheel and run `twine check` (no upload)
```

Inspect `dist/`, or install the wheel into a throwaway venv and import it, to
confirm the artifact before cutting the Release.
