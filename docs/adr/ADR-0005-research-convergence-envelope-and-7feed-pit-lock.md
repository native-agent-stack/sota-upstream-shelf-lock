# ADR-0005: Research-Convergence Envelope, 7-Feed PIT Schema (`sota-research-feeds.v2`) & 4 Strategy Archetypes

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement
While `ADR-0001..0004` locked the 18-repo 40-char SHA upstream shelf, the 5-stage promotion ladder, and the `MinTRL`/`RiskAdverseQueueModel` gates, cross-harness workflows across Mac M5 Max and Stationary `Noesis` needed a single deterministic envelope verifier uniting the 7-feed `sota-research-feeds.v2` PIT contract, the 4 strategy archetypes, 64-hex input `SHA-256` provenance, and `PHILOSOPHY_ONLY` sibling-repo authority.

## Decision Outcome
Extend `shelf_lock.research_workflow` with `CANONICAL_RESEARCH_FEEDS_V2` (`alpaca_sip`, `alpaca_boats` + `2026-12-06` `23/5` cutover flag, `alpaca_raw_vs_all_adjustment`, `sec_edgar_acceptance_datetime` `15m` half-life + `424B*`/`S-3` dilution block, `finra_regsho_cnmsshvol_t1`, `corporate_actions_split_guard`, `ibkr_paper_4002_l1`), `CANONICAL_STRATEGY_ARCHETYPES`, and `verify_research_convergence_envelope()` enforcing 18-repo 40-hex SHA match against `PINS_LOCK.json`, 64-hex `input_sha256`, `<= 2026-10-15` study wall, `MinTRL`/`MDE` power gate, `RiskAdverseQueueModel`, `ADR-0022 <= 2.00%` stop-limit, and `PHILOSOPHY_ONLY` sibling-repo authority.
