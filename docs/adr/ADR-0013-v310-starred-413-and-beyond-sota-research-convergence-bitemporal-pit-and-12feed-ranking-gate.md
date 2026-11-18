# ADR-0013: `v3.10.0` 413-Starred + Beyond-Starred SOTA Research Convergence Matrix, Bitemporal PIT & `DF1..DF12` Ranking Gate

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

While `PINS_LOCK.json` pins `18` immutable `40`-character core upstream repositories and `ADR-0005`..`ADR-0012` govern `MinTRL`/`MDE`, `RiskAdverseQueueModel`, `H096`, and `stage1_rvol_tod`, the ecosystem needed a canonical, machine-verifiable convergence matrix uniting the owner's `413` starred GitHub repositories with frontier SOTA methods beyond the starred shelf (`microsoft/RD-Agent`, `databento` bitemporal nanosecond ordering, `darts`/`statsforecast` conformal baselines, `stanfordnlp/dspy`, and ADIA Lab #19) plus finalized `DF1..DF12` Symbol Ranking DataFeed linkage under `PHILOSOPHY_ONLY` discipline.

## Decision Outcome

1. **Publish `src/shelf_lock/starred_and_beyond_matrix.py` (`sota-research-convergence-matrix.v3.10`):**
   - Registers `STARRED_413_RESEARCH_ANCHORS` (`39` high-leverage research, quant, foundation-model, skill-eval, security, and multi-runtime orchestration repos across the `413` stars) and `BEYOND_STARRED_FRONTIER_SOTA_ANCHORS` (`5` frontier SOTA anchors beyond starred) under strict `PHILOSOPHY_ONLY` authority.
   - Binds all `12` finalized Symbol Ranking DataFeeds (`DF1..DF12`) to the `18` immutable `PINS_LOCK.json` `40`-hex commits without altering the frozen `18`-pin lock.
   - Implements `verify_bitemporal_pit_event(ts_event_ns, ts_recv_ns, decision_ns)` enforcing `0 < ts_event_ns <= ts_recv_ns <= decision_ns` to prevent clock-skew and quote-arrival lookahead leakage.

## Verification Witness

- `python3 scripts/architecture_catalog.py && python3 scripts/architecture_catalog.py --check` (`13` ADRs, `0` drift), `python -m shelf_lock.validator --verify-no-leaks`, `ruff check .`, `ruff format --check .`, `pytest -q`, and `gitleaks` (`0` leaks).
