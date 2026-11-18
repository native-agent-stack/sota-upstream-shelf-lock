# ADR-0004: Pre-Registration MinTRL/MDE Power & Conservative Queue-Fill Gate

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E3

## Context and Problem Statement
Across pre-wall `Trials #1-#84`, short calendar slices (`43-67` dates) burned HLZ trial multiplicity (`t* -> 4.16`) while mathematically requiring annualized Sharpe ratios `> 8.0-10.0` to pass, and market/ask-crossing entries paid `8-16 bps` taker spread on every ignition.

## Decision Outcome
Implement `shelf_lock.research_workflow` grounded in pinned `ml4t-diagnostic` (`19e76072`, `minimum_track_record.py:160-191`, ADIA Lab #19 Eq. 11) and `hftbacktest` (`5f3ec40b`, `queue.rs:63-96`, `RiskAdverseQueueModel`):
1. Enforce `evaluate_preregistration_power_gate()` before pre-registering new trials (`distinct_dates >= 60` and `SR_min_ann <= 5.0`).
2. Model passive limit entries via `simulate_risk_adverse_buy_queue()` (strict queue depletion or trade-through) to separate spread capture from Glosten-Milgrom adverse selection.
