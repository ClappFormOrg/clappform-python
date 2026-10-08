# Releasing

Publishing to PyPI is human-gated and uses **Trusted Publishing (OIDC)**, so no
API tokens are stored in the repo. The `Release` workflow (`.github/workflows/release.yml`)
builds and verifies the distributions, then waits on the target environment's
required-reviewer approval before uploading.

The workflow has two targets:

- A **published GitHub Release** always uploads to **production PyPI**
  (`pypi.org`), gated by the `pypi` environment.
- A **manual dispatch** (Actions → Release → Run workflow) defaults to
  **TestPyPI** (`test.pypi.org`), gated by the `testpypi` environment. Use it
  to validate the OIDC + build + upload flow end-to-end without burning a real
  version on the public project. The dispatch also offers `pypi` as a target
  for a production publish without cutting a Release.

## One-time setup

Set up whichever index(es) you will publish to. TestPyPI and PyPI are
completely separate accounts and projects.

1. **Trusted publishers.** Add a GitHub Actions trusted publisher on each index:
   - Production: `clappform` at
     <https://pypi.org/manage/project/clappform/settings/publishing/> with
     **Environment: `pypi`**.
   - TestPyPI: register on <https://test.pypi.org> (the `clappform` name there is
     independent; claim it via the pending-publisher flow if it does not exist
     yet) with **Environment: `testpypi`**.

   All other fields are identical on both:
   - Owner: `ClappFormOrg`
   - Repository: `clappform-python`
   - Workflow: `release.yml`
2. **GitHub environments.** In the repository settings → Environments, create
   environments named `pypi` and `testpypi`, each with the release maintainers
   as **required reviewers**. These are the approval gates the publish job
   pauses on.

## Dry-run to TestPyPI first (recommended)

Before the first production release, validate the whole path without burning a
version:

1. Merge this workflow to the branch you will dispatch from (workflows run from
   the branch they live on).
2. Actions → **Release** → **Run workflow** → leave `target` as `testpypi` → Run.
3. The `build` job runs; the `publish` job pauses on the `testpypi` environment
   → approve it.
4. Confirm the upload at <https://test.pypi.org/project/clappform/> and, if you
   want, install it: `pip install --index-url https://test.pypi.org/simple/
   --extra-index-url https://pypi.org/simple/ --pre clappform` (the extra index
   lets dependencies resolve from real PyPI).

## Cutting a release

1. Land everything for the release on `Major/6`, then promote to the default
   branch per the branch flow.
2. Bump `__version__` in `src/clappform/__init__.py` (pre-releases use PEP 440
   suffixes, e.g. `6.0.0a1`, `6.0.0rc1`). That literal is the only place the
   version lives: `pyproject.toml` declares `dynamic = ["version"]` and
   hatchling reads it from there. Re-run `pip install -e ".[dev,pandas]"`
   afterwards, because an editable install records the version at install time
   and `test_version_matches_packaged_version` compares against it. Commit.
3. Tag and publish a **GitHub Release** whose tag matches the version
   (`v6.0.0a1` or `6.0.0a1`). Put the release notes, including the proto diff
   of the sync, in the release body.
4. The `Release` workflow runs: it builds the sdist + wheel, fails if the tag
   and the built wheel's version disagree, and validates metadata with
   `twine check`.
5. The `publish` job then pauses on the `pypi` environment. A required reviewer
   approves, and only then does the upload run.

Pre-releases (`aN`/`bN`/`rcN`) are not installed by a plain `pip install
clappform`; users opt in with `pip install --pre clappform` or a pinned
`clappform==6.0.0a1`.

## Verifying locally before you tag

```bash
make release-check   # build sdist+wheel and run `twine check` (no upload)
```

`make release-check` needs `twine>=7.0` from the `dev` extra: hatchling stamps
Metadata 2.5, and twine 6.x rejects it with `'2.5' is not a valid metadata
version`. Run `pip install -U -e ".[dev]"` if you hit that.

Check the version is still free on whichever index you are targeting. Neither
PyPI nor TestPyPI accepts a re-upload of a version that already exists, and the
two indexes hold different sets:

```bash
python - <<'EOF'
import json, urllib.request
for host in ("pypi.org", "test.pypi.org"):
    with urllib.request.urlopen(f"https://{host}/pypi/clappform/json") as r:
        print(host, sorted(json.load(r)["releases"]))
EOF
```

Inspect `dist/`, or install the wheel into a throwaway venv and import it, to
confirm the artifact before cutting the Release.
