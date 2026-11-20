# ADR-0020: Advanced Strategy Sources, Frontier OSS Libraries/Repos (40-Char SHA & SPDX Verified) & License-Firewall Convergence for Sim-to-Merit Backtesting

- **Status:** Accepted
- **Date:** 2026-11-20
- **Evidence Grade:** E4 (`STARRED_CONVERGENCE_CATALOG.json`, `tests/test_adr0020_advanced_strategy_sim_merit_landscape.py`, live `gh api` 40-char SHA + verbatim `LICENSE` inspection across `25+` repositories, primary SSRN/arXiv/JF/JFE/RFS/Econometrica DOI verification, `scripts/architecture_catalog.py --check`, `pytest`, `ruff`, `gitleaks 0`)
- **GitHub Evidence:** https://github.com/bashtage/arch/commit/d3e858fc1c99932bb6936cbaf0d1b45b136266e5, https://github.com/scikit-learn-contrib/MAPIE/commit/e4c4f5f7daeaa7c8b09323852ad1997e506891a2, https://github.com/delta-io/delta-rs/commit/36b8bd2906d7f643f4cd8c5e2dc1c57790b5b945, https://github.com/online-ml/river/commit/5ea245400645aba5239e4fcb19b59b756d2e9e53, https://github.com/databento/dbn/commit/684641e33eba3008338762ea1e1e43904f32072f, https://github.com/microsoft/qlib/commit/54355232463878d2eebb91fe0ee5fa7fa1f5976c, https://github.com/openbq-org/OpenBB/commit/5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0

## Context and Problem Statement

To expand our 5-stage `Sim -> Pre-Wall Backtest -> Paper -> Empirical-Bayes Merit -> Broker` manifest pipeline beyond the existing 18 immutable core shelf pins (`ADR-0001`), the ecosystem required a primary-source, license-audited convergence across (a) 2021–2026 institutional equity strategy & statistical validation literature and (b) maintained open-source quant, bitemporal lake, conformal uncertainty, streaming drift, causal inference, and hierarchical Bayesian repositories. Live `2026-11-20` primary-source auditing also surfaced three urgent upstream changes affecting `ADR-0018` (`microsoft/qlib v0.9.8` AST/pickle security hardening; archival of `OpenBB-finance/backends-for-openbb` in favor of `openbq-org/backends-for-openbb`; relicensing of `openbq-org/OpenBB v5.0.0` from `AGPL-3.0-only` to `Apache-2.0`) and confirmed verbatim non-permissive license walls on `cvxportfolio` (`GPL-3.0`), `freqtrade` (`GPL-3.0`), `backtesting.py` (`AGPL-3.0`), `pybroker` (`Commons Clause v1.0`), `ArcticDB` (`BUSL-1.1`), and `mlfinlab` (`Proprietary`).

## Decision Outcome

1. **Preserve all 18 immutable `PINS_LOCK.json` core pins and `ADR-0017`/`ADR-0018`/`ADR-0019` blocks byte-for-byte** (`immutableCorePinsUntouched = 18`).
2. **Add additive `advancedStrategyAndSimMeritLandscape` block (`schemaId: sota-v3113-advanced-strategy-sim-merit-landscape.v1`)** to `STARRED_CONVERGENCE_CATALOG.json`:
   - **18 ROI-Ranked Permissive Frontier Libraries** with live-verified 40-char GitHub commit SHAs, exact SPDX licenses, `orderAuthority = false`, and explicit `requiresValidatorLicenseAdr` flags for OSI-permissive `NCSA` (`bashtage/arch`, `bashtage/linearmodels`).
   - **3 `ADR-0018` Upstream Security & License Advisories** (`qlib v0.9.8`, `openbq-org/backends-for-openbb`, `openbq-org/OpenBB v5.0.0 Apache-2.0`).
   - **7 License-Firewall / Archived Exclusions** (`PHILOSOPHY_ONLY`, zero code import): `cvxportfolio` (`GPL-3.0`), `freqtrade` (`GPL-3.0`), `backtesting.py` (`AGPL-3.0`), `pybroker` (`Commons Clause v1.0`), `ArcticDB` (`BUSL-1.1`), `mlfinlab` (`Proprietary`), and `abides-jpmc-public` (`Archived June 2025`).
   - **6 Primary-Literature Frontier Strategy & Validation Families (`F1..F6`)** with verified DOIs/arXiv/SSRN URLs mapped cleanly to current datafeed readiness (`SIP+BOATS`, `edgartools v6.2.0`, `ml4t-diagnostic v0.2.0`) vs. future L2/L3 `Databento DBN` + `NOII` onboarding.
3. **Strict Governance & Zero Trial Consumption:** Ships strictly as `PROTECTIVE_FILTER_OR_GOVERNANCE` (`standaloneAlphaClaim = false`, `hlzTrialConsumed = false`, preserving `Trial #105` `t*(105) = 4.2084`); live broker ports (`4001`, `7496`, `8796`, `8798`) and hosts (`api.alpaca.markets`) remain 100% hard-refused.

## Alternatives Considered

- **Mutate `PINS_LOCK.json` or `validator.py::ALLOWED_LICENSES` simultaneously without downstream lock parity:** Rejected — keeps the 18 immutable core pins (`ADR-0001`) unbroken across all 18 ecosystem repositories while giving every repo a single SHA-verified catalog of approved next-wave research extensions.
- **Adopt `cvxportfolio`, `ArcticDB`, or `pybroker` directly:** Rejected — verbatim `LICENSE` audits confirmed `GPL-3.0`, `BUSL-1.1`, and `Commons Clause v1.0` restrictions outside `ALLOWED_LICENSES`; replaced cleanly with `cvxpy + Clarabel.rs` (`Apache-2.0`) and `delta-rs + duckdb/ducklake` (`Apache-2.0` / `MIT`).

## Verification Witness

- Enforced by `tests/test_adr0020_advanced_strategy_sim_merit_landscape.py`, `tests/test_shelf_lock.py`, `scripts/architecture_catalog.py --check` (`20/20` ADRs, `0` drift), `ruff check .`, `ruff format --check .`, and `gitleaks protect --staged --no-banner` (`0` leaks).

## Rollback

Revert the single commit adding `advancedStrategyAndSimMeritLandscape` and `ADR-0020`; all 18 core pins and `ADR-0001..0019` remain unchanged.
