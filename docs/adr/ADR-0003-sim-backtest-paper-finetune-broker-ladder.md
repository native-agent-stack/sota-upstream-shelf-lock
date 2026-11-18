# ADR-0003: Five-Stage Compounding Strategy Promotion Ladder (`Sim -> Backtest -> Paper -> Fine-Tune -> Alpaca/IBKR`)

- **Status:** Accepted
- **Date:** 2026-11-17
- **Evidence Grade:** E3 (Enforced by `shelf_lock.validator.validate_promotion_candidate`)

## Context and Problem Statement

Promoting candidate alpha factors or trailing-stop rules directly from raw OHLCV backtests or small paper cohorts (`n < 30`) produces severe multiple-testing and spread-crossing decay (`H05` / `H06`).

## Decision Outcome

Every strategy candidate must clear five sequential, machine-checked stages in [`PINS_LOCK.json`](../../PINS_LOCK.json):
1. **`SIM_EVENT_PARITY` (`native-agent-stack/meridian`):** Queue-position & spread fill parity (`nautilus_trader` + `hftbacktest`).
2. **`BACKTEST_PREWALL_STAT_GATE` (`<= 2026-10-15`):** Date-clustered `t >= t*(N)` (Harvey–Liu–Zhu), native-frequency `DSR > 0.95`, `CombinatorialPurgedCV` `PBO < 0.25`, and `net_2x_cost_bps > 0`.
3. **`PAPER_24X5_EXECUTION` (`sota-mover-ranker` + `sota-dynamic-trail-c`):** Atomic `ADR-0022 <= 2.00%` stops, `<= 200 req/min` Alpaca Paper + `<= 3,000 msg/min` IBKR (`:4002`) pacing, and `60s` dead-man supervision.
4. **`EMPIRICAL_BAYES_FINETUNE` (`sota-private-vault`):** `n_closed >= 30` closed paper trades with pre-registered `Dec 6, 2026` `23/5 SIP` regime split.
5. **`BROKER_PROMOTION_READINESS`:** 100% owner-gated sign-off (autonomous live-account access remains hard-refused).
