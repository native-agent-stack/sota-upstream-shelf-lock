# ADR-0023: Universal Hard SOTA Upstream-Source, Zero-Escape-Hatch Engine Binding & ADR-Evidence Rule

- **Status:** Accepted
- **Date:** 2026-11-20
- **Layer:** Org-Wide Source Provenance, Strategy/Backtest Engine Hygiene & ADR/Manifest Evidence Firewall (`PROTECTIVE_FILTER_OR_GOVERNANCE`, `standalone_alpha_claim = False`)
- **Evidence Grade:** E4 (`src/shelf_lock/hard_upstream_rule.py`, `upstream-map.toml`, `scripts/merge_gate.py`, `tests/test_adr0023_hard_upstream_rule.py`, `pytest`, `ruff`, `architecture_catalog.py --check`, `merge_gate.py`, `gitleaks 0`, and 18-repo workstation audit receipt)
- **GitHub Evidence:** https://github.com/native-agent-stack/sota-upstream-shelf-lock, https://github.com/nautechsystems/nautilus_trader/commit/da6b57aefdd62b44f675e434ffcfefca7f4025dd, https://github.com/nkaz001/hftbacktest/commit/5f3ec40b2afb764e0fea112f941ed85523ef4e88, https://github.com/polakowo/vectorbt/commit/a52a984b631624bb9daf41cb19f532fe559cf0ef
- **Revisit Trigger:** Multi-repo pin cutover of `PINS_LOCK.json` or onboarding of a new repository into `native-agent-stack`.

## Context and Problem Statement

An ecosystem-wide provenance audit (`2026-11-20`) revealed uneven mechanical enforcement of the owner's upstream-first mandate across the 18 active `native-agent-stack` repositories:
1. Only `meridian`, `astrolabe`, `canon`, `sota-mover-ranker`, `sota-dynamic-trail-c`, and `agy-sota-harness` mechanically enforced file-to-upstream mapping on commit/merge; `sota-compounding-lab`, `sota-upstream-shelf-lock`, and `sota-multi-model-workflows` lacked mechanical `upstream-map.toml` validation in `scripts/merge_gate.py`.
2. Strategy, backtest, and simulation engine modules could previously pass syntactic map checks by citing bare `"cpython-stdlib"` or `"academic-momentum-literature"` without binding to a real maintained SOTA upstream library (`nautilus_trader`, `hftbacktest`, `vectorbt`, `skfolio`, `ml4t-diagnostic`, `statsmodels`, `arch`, `polars`, `duckdb`, `pandera`, `exchange_calendars`, `alpaca-py`, `ib_async`, `edgartools`).
3. No single fail-closed library verified simultaneously across repos that every MADR 4.0 ADR carries verifiable evidence and every sealed JSON manifest carries a finite cryptographic digest with zero leaks.

## Decision Outcome

1. **Enact `src/shelf_lock/hard_upstream_rule.py` (`sota.hard-upstream-source-rule.v1`) as the universal hard provenance contract:**
   - **Rule 1 (Zero Orphan Code):** Every tracked implementation file must map in `upstream-map.toml` (`how in {"install", "integrate", "build-on"}`, non-empty `feature` and `why`) to a registered entry in `UPSTREAM.md`; unused patterns fail closed.
   - **Rule 2 (No Bespoke Sim/Backtest/Strategy Escape Hatches & Zero Low-Quality Banned Libs):** Active strategy, backtest, and simulation engine patterns must bind to a real maintained SOTA upstream library (refusing bare `cpython-stdlib` / `academic-momentum-literature` sole provenance and hard-refusing `yfinance`, `backtrader`, `backtesting.py`, abandoned `mlfinlab`, `tcapy`, `vollib`, `abides-jpmc-public`, `tradingview_ta`, `pandas-datareader`).
   - **Rule 3 (Every ADR & Sealed Manifest Carries Evidence):** Every ADR in `docs/adr/*.md` must contain explicit evidence/witness provenance, and every `docs/*MANIFEST*.json` must be strict finite JSON (`allow_nan=False`) carrying `manifest_sha256` with zero home-path, account-ID, or secret leaks.
   - **Rule 4 (Immutable 18-Pin Shelf Parity):** All 18 read-only clones in `~/Documents/upstream/` must sit cleanly on their exact 40-char `PINS_LOCK.json` SHAs.
2. **Enforce locally in `sota-upstream-shelf-lock` via `upstream-map.toml` + `scripts/merge_gate.py`** and propagate identical fail-closed enforcement to `sota-compounding-lab` and `sota-multi-model-workflows`.

## Alternatives Considered

- **Leave upstream-first enforcement as prose guidelines in `AGENTS.md`:** Rejected per explicit owner mandate; prose rules drift without deterministic fail-closed merge gates.

## Verification Witness

- `pytest -q` (including `tests/test_adr0023_hard_upstream_rule.py` covering positive/negative upstream maps, banned low-quality libraries, bespoke engine rejection, ADR evidence enforcement, manifest digest checks, and workstation audit).
- `python scripts/merge_gate.py` -> `[MERGE-GATE PASS]`.
- `python scripts/architecture_catalog.py --check` -> `23 ADRs valid, 0 drift`.
- `ruff check .` & `gitleaks protect --staged --no-banner` (`0` leaks).
