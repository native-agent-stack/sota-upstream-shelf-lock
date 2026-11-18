# ADR-0001: Immutable 40-Character Git SHA Pinning Across All 18 Quantitative & Execution Upstreams

- **Status:** Accepted
- **Date:** 2026-11-17
- **Evidence Grade:** E3 (Online `git ls-remote` & Local Shelf Verified)

## Context and Problem Statement

Floating tags or unpinned package ranges introduce silent upstream regressions across market-data ingestion (`alpaca-py`, `polars`, `duckdb`, `edgartools`), simulation (`nautilus_trader`, `hftbacktest`), statistical falsification (`skfolio`, `ml4t-diagnostic`, `statsmodels`), execution (`ib_async`, `alpaca-mcp-server`), and UI blotters (`lightweight-charts`, `perspective`).

## Decision Outcome

Pin all 18 `T1–T8` upstreams by exact 40-character hexadecimal Git commit SHA and verified SPDX license in [`PINS_LOCK.json`](../../PINS_LOCK.json), attested automatically on every push, PR, and daily scheduled GitHub Action via `shelf_lock.validator --online`.
