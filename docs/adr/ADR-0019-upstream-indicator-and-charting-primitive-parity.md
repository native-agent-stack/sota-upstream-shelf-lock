# ADR-0019: Pinned Upstream Indicator & Charting Primitive Parity (`nautilus_trader` 39 Native Rust Indicators, `lightweight-charts` 29 Plugins, `hftbacktest` Microstructure & Uncapped Pine v6 Suite)

- **Status:** Accepted
- **Date:** 2026-11-20
- **Evidence Grade:** E4
- **GitHub Evidence:** https://github.com/nautechsystems/nautilus_trader/commit/da6b57aefdd62b44f675e434ffcfefca7f4025dd, https://github.com/nkaz001/hftbacktest/commit/5f3ec40b2afb764e0fea112f941ed85523ef4e88, https://github.com/tradingview/lightweight-charts/commit/c29c51e1e5bc61981da5832c97797cb8283d120f, https://github.com/finos/perspective/commit/0264ec13cd28ef4a2a136c8ef021c3c112bc8990

## Context and Problem Statement

While `ADR-0001`, `ADR-0017`, and `ADR-0018` lock the 18 immutable core shelf repositories and terminal platform taxonomy, the exact upstream indicator libraries and charting Series Primitives mirrored into `sota-mover-ranker` (`ranker/tv_upstream_indicator_landscape.py` and `tradingview_suite/*.pine`) needed a formal catalog provenance block verifying exact 40-char commit SHAs, accurate native indicator/plugin counts, dual Lightweight Charts runtime/reference asset tracking, zero alert/webhook execution authority (`ADR-0017`), and uncapped lossless parity.

## Decision Outcome

1. **Preserve all 18 immutable `PINS_LOCK.json` pins, `ADR-0017` `terminalPlatformTaxonomy`, and `ADR-0018` `alphaFactoryAndTerminalExtensions` byte-for-byte.**
2. **Add additive `upstreamIndicatorAndChartingPrimitives` block (`schemaId: sota-v3112-upstream-indicator-primitives.v1`)** to `STARRED_CONVERGENCE_CATALOG.json`:
   - Records verified first-hand upstream counts and mirrored formulas across `nautilus_trader@da6b57aefdd6` (39 native Rust `impl Indicator` files excluding Python PyO3 wrappers: `EfficiencyRatio`, `SpreadAnalyzer` spot spread gate reference in `paper_auto_engine.py`, `AdaptiveMovingAverage`, `Pressure`, `KlingerVolumeOscillator`, `KeltnerChannel`, `BollingerBands`, `VWAP`), `hftbacktest@5f3ec40b2afb` (Stoikov microprice, CKS-2014 OFI proxy, `RiskAdverseQueueModel` lot-rounded queue fill reference in `queue.rs` with lit round-lot print-eligibility filter in `protective_entry_shield.py`), `lightweight-charts@c29c51e1e5bc` (29 official Series Primitives: `volume-profile`, `session-highlighting`, `bands-indicator`, `user-price-lines`, `delta-tooltip`, plus dual-asset pointer to deployed npm runtime `5.0.8@c65d0697ad0c`), and `perspective@0264ec13cd28` (`v5.9.2`).
   - Enforces `orderAuthority = false`, `visualArtifactsMayBindAlertOrWebhook = false`, `takeProfitCapEnabled = false`, `standaloneAlphaClaim = false`, and live broker port/host refusal (`4001`, `7496`, `8796`, `8798`, `api.alpaca.markets`).
   - Registers the 7 canonical uncapped Pine v6 strategies (`Strategy_1..6` + `SOTA_Early_Mover_Bracket_Strategy.pine`) and `SOTA_Master_All_In_One_24x5_Indicator.pine`.

## Alternatives Considered

- **Add third-party TA libraries to `PINS_LOCK.json` beyond 18 immutable pins:** Rejected; breaks `ADR-0001` 18-pin immutability when `nautilus_trader` already provides 39 institutional native Rust indicators on the pinned shelf.

## Verification Witness

- Enforced by `tests/test_upstream_indicator_catalog_parity.py`, `tests/test_shelf_lock.py`, `scripts/architecture_catalog.py --check`, `shelf_lock.validator --verify-no-leaks`, `ruff`, `gitleaks 0`, and cross-vendor Pass-2 red-team verification.

## Rollback

Revert the single commit adding `upstreamIndicatorAndChartingPrimitives` and `ADR-0019`; all 18 core pins, `ADR-0017`, and `ADR-0018` remain unchanged.
