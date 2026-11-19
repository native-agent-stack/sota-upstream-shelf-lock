# ADR-0014: `v3.10.6` Live Upstream Shelf Audit, `DF1..DF12` Doc Convergence & Retired-Runtime Hygiene

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

While `ADR-0013` introduced the `v3.10` 413-starred + beyond-starred convergence matrix and `DF1..DF12` Symbol Ranking DataFeeds, `UPSTREAM.md` and `PINS_LOCK.json` (`verifiedDate: 2026-11-17`) still listed stale `v3.9.0` runtime metadata (`DF1..DF9`-only header, `oh-my-claudecode v5.8.4`, `16` `run_workflow` DAGs on `gemini-4-carbon-high`, and retired `block/goose v1.59.2`). Furthermore, live GitHub release checks on `2026-11-18` identified `8` minor/patch upstream releases ahead of the frozen `18`-pin lock (`edgartools v6.3.0`, `ml4t-diagnostic v0.2.1`, `skfolio v1.13.0`, `perspective v5.9.3`, `lightweight-charts master`, `vectorbt v1.2.1`, `pandera v0.36.0`, `exchange_calendars 4.13.3`) while all `18/18` local workstation shelf clones and downstream `upstream-map.toml` / `uv.lock` constraints remain pinned to the regression-tested SHAs.

## Decision Outcome

1. **Preserve Immutable `18`-Pin `40`-Char SHAs (`ADR-0001` / `ADR-0013`):** Keep all `18` `PINS_LOCK.json` commit SHAs untouched so cross-repo `sota-mover-ranker/upstream-map.toml`, `~/Documents/upstream`, and pre-wall `uv.lock` reproducibility remain `18/18` zero-drift, while advancing `PINS_LOCK.json` `verifiedDate` to `2026-11-18`.
2. **Converge `UPSTREAM.md` to `v3.10.6`:** Update the active orchestration summary to `DF1..DF12` (`DF1..DF9` compat), `57` canonical skills, `20` `run_workflow` DAGs (`gemini-4-neon-xhigh` flagship + `gemini-4-carbon-high`), `oh-my-claudecode v5.8.6`, and explicitly record `block/goose` and `grok` as retired.
3. **Publish Live Audit Ledger:** Record the `10` `CURRENT` pins and `8` evaluated-and-held minor/patch candidates inside `UPSTREAM.md` Section 3 so the next scheduled multi-repo lockfile bump has an audited, auditable baseline.

## Verification Witness

- `uv run python scripts/architecture_catalog.py --check` (`14` ADRs, `0` drift), `uv run python -m shelf_lock.validator --verify-no-leaks --online`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest -v`, and `gitleaks --staged` (`0` leaks).
