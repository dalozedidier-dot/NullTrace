# NullTrace

A minimal, reproducible, CI-stable baseline for deterministic soak testing and artifact generation.

## Design rules

- Strict `src/`-only Python layout
- Only two workflows: `ci` and `mass-nulltrace`
- No auto-fix / auto-commit workflows
- Deterministic artifacts written to `_ci_out/mass/`

## Quick usage

Local (optional):

- `python -m pip install -r requirements.txt -r requirements-dev.txt`
- `pytest -q`
- `python -m tools.nulltrace_soak --runs 3 --out-dir _ci_out/mass`

In GitHub Actions:

- `ci` runs on Python 3.10/3.11/3.12
- `mass-nulltrace` runs on schedule or manually and uploads `_ci_out/mass`
