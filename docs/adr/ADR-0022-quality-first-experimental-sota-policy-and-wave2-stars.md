# ADR-0022: Quality-and-SOTA-Only Experimental Repo Evaluation Policy & Wave-2 Frontier SOTA Star Expansion (`108` Total New Stars)

- **Status:** Accepted
- **Date:** 2026-11-20
- **Evidence Grade:** E4 (`STARRED_CONVERGENCE_CATALOG.json`, `src/shelf_lock/validator.py`, `tests/test_adr0022_quality_first_experimental_policy.py`, `58/58` Wave-2 + `50/50` Wave-1 = `108/108` live GitHub stars & 40-char HEAD SHAs verified `2026-11-20`, `scripts/architecture_catalog.py --check`, `pytest`, `ruff`, `ty` `0` diagnostics, `gitleaks 0`)
- **GitHub Evidence:** https://github.com/cvxgrp/cvxportfolio/commit/351c782b9b8b395c1a5f886b77e0d55f1bc9396e, https://github.com/man-group/ArcticDB/commit/2f7f5ba8288ea64c616548e593c1948868c314ea, https://github.com/google-research/timesfm/commit/918df02c9d366b2145bc5876135fa2131d3ed2a6, https://github.com/xtdb/xtdb/commit/efca88aad2e074d0db470eacce9416d7979d629d, https://github.com/ml4t/backtest/commit/99ee9970f74dbde59d2863189108146fc60e9685, https://github.com/Nixtla/conformalforecast/commit/59922b75adbc377342f68c453ff0d8fc6dcc7532, https://github.com/NVIDIA/cudf/commit/ece1ff92c8e5a61ac87f6cc43ef5cf763659377d

## Context and Problem Statement

Per explicit owner directive (`2026-11-20`), the `native-agent-stack` environment operates strictly as a personal, effectively-private experimental workstation (zero external stars/watchers, zero external redistribution). Prior `ADR-0020`/`ADR-0021` license-firewall exclusions blocked technically world-class libraries solely on license tags (`cvxgrp/cvxportfolio`, `man-group/ArcticDB`, `google-research/timesfm`, `xtdb/xtdb`, `edtechre/pybroker`, `freqtrade/freqtrade`). Additionally, live GitHub organization sweeps uncovered 58 high-craft frontier repositories (`ml4t/*` 2026 modular suite, Stanford `cvxgrp/*`, `SalesforceAIResearch/uni2ts`, `ibm-granite/granite-tsfm`, `thuml/Time-Series-Library`, `autogluon`, `Nixtla/conformalforecast`, `aangelopoulos/conformal-time-series`, `alphanome-ai/sec-parser`, `nautechsystems/nautilus_agents`, `NVIDIA/cudf` + `NVIDIA/cuml`, `ray`, `triton`, `datafusion`, `dspy`, etc.) missing from the owner's stars.

## Decision Outcome

1. **Codify `EXPERIMENTAL_ENV_EVALUATION_POLICY = "QUALITY_AND_SOTA_ONLY_NO_LICENSE_EXCLUSION"`** in `src/shelf_lock/validator.py` with `evaluate_experimental_repo_eligibility()` evaluating strictly on maintenance health, institutional/SOTA caliber, verifiable data provenance, and multi-asset depth — **never excluding a technically SOTA repo on license tags** inside this personal experimental environment.
2. **Add `experimentalQualityFirstSotaExpansion` (`schemaId: sota-v3115-experimental-quality-first-sota.v1`)** to `STARRED_CONVERGENCE_CATALOG.json`:
   - Preserves all **18 immutable core pins in `PINS_LOCK.json`** byte-for-byte (`SHA-256` verified).
   - Unblocks all **6 technically world-class libraries previously excluded only on license** (`cvxportfolio`, `ArcticDB`, `timesfm`, `xtdb`, `pybroker`, `freqtrade/FreqAI`) with verified 40-char SHAs.
   - Seals **19 Wave-2 flagship SOTA additions** with 40-char SHAs and the **`58/58` Wave-2 (`108` cumulative today)** GitHub Star Sync Receipt.
   - Keeps **strictly technical-quality rejections** (`yfinance`, `backtrader`, `backtesting.py`, abandoned `mlfinlab`, stale `tcapy`/`vollib`, archived `abides-jpmc-public`, unofficial TradingView scrapers).
3. **Zero Trial Consumption & Paper-Only Firewall:** `PROTECTIVE_FILTER_OR_GOVERNANCE`, `standaloneAlphaClaim = false`, `hlzTrialConsumed = false`, preserving `Trial #105` `t*(105) = 4.2084`.

## Alternatives Considered

- **Retain third-party redistribution license walls inside a zero-redistribution personal lab:** Rejected per owner direction; technical SOTA rigor governs experimental adoption.

## Verification Witness

- `scripts/architecture_catalog.py --check` (`22/22` ADRs, `0` drift), `pytest -q`, `ruff check .`, `ruff format --check .`, `ty check` (`0` diagnostics across whole repo), and `gitleaks protect --staged --no-banner` (`0` leaks).

## Rollback

Revert the single `ADR-0022` commit; `PINS_LOCK.json` and `ADR-0001..0021` remain untouched.
