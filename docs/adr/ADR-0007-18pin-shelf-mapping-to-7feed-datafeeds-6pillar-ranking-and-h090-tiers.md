# ADR-0007: 18-Pin Upstream Shelf Mapping to 7-Feed PIT DataFeeds, 6-Pillar Ranking & `H090` Execution Tiers (`v3.8.0`)

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

Building on `ADR-0005` (`sota-research-feeds.v2` 7-feed PIT envelope) and `ADR-0006` (`H085 -> H088 -> H089` two-stage queue synthesis), finalizing the `v3.8.0` Trading Ranking System (`sota-ranking-and-datafeeds.v2`) required an explicit 1:1 architectural mapping from the `18` immutable `40`-char Git SHA pins in `PINS_LOCK.json` to every DataFeed, Ranking Pillar, and Execution-Quality Tier (`Trial #90 H090`).

## Decision Outcome

1. **Authoritative 18-Pin Upstream -> 7-Feed DataFeed & 6-Pillar Ranking Bijection:**
   - **Feed & Microstructure Layer:** `alpacahq/alpaca-py` (`SIP`/`BOATS`/`RAW`-vs-`ALL`), `dgunning/edgartools` (`acceptanceDateTime` `15m` half-life + `S-3`/`424B*` dilution shield), `gerrymanoim/exchange_calendars` (`XNYS` `RVOL_tod` buckets & `bar_age_sessions == 0` Stockbee freshness gate), `ib-api-reloaded/ib_async` (`:4002` shortable/fee L1 & `2,700/300` reserve), `pola-rs/polars` + `duckdb/duckdb` + `unionai-oss/pandera` (schema-locked Parquet compounding lake).
   - **Queue, Simulation & Statistical Gate Layer:** `nkaz001/hftbacktest` (`RiskAdverseQueueModel` `bs * 100.0` round-lot shares powering `H090` `TIER1` `<= 10 bps` / `OFI >= 25%` passive fills and `H089` `TIER2` two-stage hybrid joins), `nautechsystems/nautilus_trader` (`v2.0.0rc9` event-driven simulation parity), `ml4t/diagnostic` (`ADIA #19 MinTRL/MDE` + `DSR`), `skfolio/skfolio` (`CombinatorialPurgedCV` confirming `H090` `5/5` positive OOS paths), `statsmodels/statsmodels` (date-clustered SEs), `polakowo/vectorbt` + `ranaroussi/quantstats` (pre-wall tear-sheets), and `tradingview/lightweight-charts` + `finos/perspective` + `alpacahq/alpaca-mcp-server` + `JoshData/python-email-validator` (blotter, watchlists, and schema hygiene).
2. **Zero Unpinned Dependencies (`PHILOSOPHY_ONLY` Sibling & External Reference Rule):**
   - External frameworks outside `PINS_LOCK.json` (`QuantConnect/Lean` `RelativeDailyVolume.cs`, Stockbee EP/Momentum-Burst heuristics) enter strictly as clean-room, Hypothesis-tested formulas (`sota-compounding-lab` `ADR-0010`) without unpinned runtime imports.

## Alternatives Considered

1. **Import unpinned third-party screening packages directly into the live `:8787` ranking loop:** Rejected — violates `ADR-0001` supply-chain immutability and `PINS_LOCK.json` determinism.
2. **Omit `H090` spread/`OFI` execution-quality tiering from the shelf-to-ranking contract:** Rejected — `H090` proved `<= 10 bps` + `OFI >= 25%` eliminates toxic passive-bid sweep adverse selection (`+20.84 bps` 1x, `5/5` `CPCV`).

## Verification Witness

- `python3 scripts/architecture_catalog.py` + `python3 scripts/architecture_catalog.py --check` (`7/7` Accepted ADRs, `0` drift).
- `uv run --extra dev pytest -q`, `ruff check .`, & `gitleaks detect --no-git --no-banner` (`100% PASS`, `0` leaks).
