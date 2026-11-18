# ADR-0006: Two-Stage `RiskAdverseQueueModel` Synthesis (`H085` -> `H088` -> `H089`), `cc-lead` 14-Workflow Hub & 89-Trial HLZ Convergence

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

Building on `ADR-0004` (`ADIA Lab #19 MinTRL/MDE` + `hftbacktest::RiskAdverseQueueModel`) and `ADR-0005` (`sota-research-feeds.v2` 7-feed PIT envelope), three pre-registered nanosecond `SIP` pre-wall (`<= 2026-10-15`) trials (`Trial #85 H085`, `Trial #88 H088`, and `Trial #89 H089` across `14,750` symbol-day pairs and `587` dates) evaluated passive queue physics against right-tail runner censoring while the ecosystem converged on Claude Code (`cc-lead`, `claude-fable-5-2` `xhigh` + `OMC` Runtime v2) as central `14`-workflow runtime orchestrator.

## Decision Outcome

1. **Empirical Queue-Fill & Skewness Synthesis (`PINS_LOCK.json` `hftbacktest` `@ 5f3ec40b` + `ml4t-diagnostic` `@ 19e76072`):**
   - Pure passive `10:30` ET `RiskAdverseQueueModel` (`bs * 100.0` CTA/UTP round-lot shares) fills `86.41%` (`H085`) and cuts `CVaR_95` by `-44.55%` when paired with a `+60 bps` micro Gain-Lock (`H088`), but misses `13.17%` of runaway breakouts and censors `97.8%` of right-tail RTH runners.
   - Pairing Two-Stage Hybrid Entry (`50%` passive queue in `120s` + `50%` passive depletion or `120s` runaway join) with `50/50` Core-Harvest + Zero-Loss Breakeven Runner Convexity (`H089`) restores `95.50%` participation, expands `15:55` ET runner survival `23x` (`2.20% -> 50.75%`), and compresses date-clustered `SE` `-42.4%` (`9.70 -> 5.588 bps`) under dynamic Harvey–Liu–Zhu multiplicity (`N = 89 -> t*(90) = 4.1735`).
2. **Enforce `18`-Pin Shelf Cleanliness Across `cc-lead` Multi-Runtime Workers (`Mac M5 Max <-> Noesis`):**
   - All `14` self-bootstrapping workflows (including `cc_lead_multi_runtime_workers_workflow.py` `#14` and `sota-cc-hub`) verify `18/18` clean `40`-char upstream shelf pins (`PINS_LOCK.json`) across both `Mac M5 Max` and stationary `Noesis` (`15/15` cross-OS runtime binary parity) before dispatching any research or promotion worker.

## Alternatives Considered

1. **Substitute optimistic mid-quote fills or unscaled `bs` share units (`1x` instead of `100x` round lots):** Rejected — overstates passive fill rates and masks Glosten–Milgrom adverse selection (`ADR-0004`).
2. **Reset or prune `N = 89` failed pre-wall trials from the HLZ hurdle:** Rejected — induces selection bias in `evaluate_preregistration_power_gate(cumulative_trials_n=N)`.

## Verification Witness

- `python3 scripts/architecture_catalog.py` + `python3 scripts/architecture_catalog.py --check` (`6/6` Accepted ADRs, `0` drift).
- `pytest -q`, `ruff check .`, & `gitleaks detect --no-git --no-banner` (`100% PASS`, `0` leaks).
