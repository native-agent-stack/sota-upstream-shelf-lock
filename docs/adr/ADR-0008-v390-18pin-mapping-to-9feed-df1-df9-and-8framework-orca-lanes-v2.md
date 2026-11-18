# ADR-0008: v3.9.0 18-Pin Shelf Mapping to 9-Feed `sota-ranking-datafeeds.v3.8` (`DF1–DF9`), 8-Framework Matrix & `UPSTREAM.md`

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

Following `ADR-0007`, ecosystem `v3.9.0` (`sota-multi-model-workflows` `ADR-0016`, `sota-harness-foundation` `ADR-0031`) expanded the canonical DataFeed contract to **`9` PIT Ranking System DataFeeds (`DF1..DF9`, `sota-ranking-datafeeds.v3.8`)**, anchored the `64`-hex `prewallLakeSha256` (`a253421e873441740d5d4b410d993cfa7345fe34b88ec4ab7f4eecd537b3f234`), and required root `UPSTREAM.md` coverage across all `17` active code/research repositories.

## Decision Outcome

1. **Publish `UPSTREAM.md` & Bind `18` `40`-Hex Shelf Pins (`cb34b0c35043...`) to `DF1..DF9` and `H2` Orca Lane Hub v2:**
   - Map `alpaca-py` (`DF1`/`DF2`), `polars` (`DF3`), `exchange_calendars` (`DF4`/`DF8`), `edgartools` (`DF5`/`DF6`), `duckdb` (`DF7`), `ib_async` (`DF9`), `hftbacktest` (`RiskAdverseQueueModel`), `skfolio` (`CPCV`), and `ml4t-diagnostic` (`DSR`) alongside all `8` SOTA multi-model orchestration frameworks (`17` binaries, `7` vendors).

## Verification Witness

- `python3 scripts/architecture_catalog.py` & `--check`, `python3 -m unittest discover -s tests` (or repo tests), and `gitleaks detect --no-git --no-banner` (`0` leaks).
