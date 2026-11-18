# ADR-0012: `v3.9.9` Whole-Market Abnormal-Over-Normal Time-of-Day `RVOL` (`stage1_rvol_tod`) Size-Bias Purge Gate

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

Raw cumulative dollar/share volume screens suffer structural mega-cap size bias, admitting liquid mega-caps trading at ordinary normal rates (`1.01x` or `0.70x` of their 20-day time-of-day baseline) into `First Sign` and `Early Stage Potential` buckets ahead of genuine whole-market abnormal volume shocks (`QuantConnect/Lean` `RelativeDailyVolume.cs` lineage).

## Decision Outcome

1. **Publish `evaluate_abnormal_rvol_tod_shelf_gate` (`src/shelf_lock/research_workflow.py`):**
   - Compute `stage1_rvol_tod = observed_cum_vol / expected_20d_tod_vol`, purge normal-rate mega-cap size bias (`stage1_rvol_tod < 1.65`), require `stage1_rvol_tod >= 1.65` with `ofi_entry > 0` for `First Sign`, and require `stage1_rvol_tod >= 2.20` with `ofi_entry >= 0.25` for `Early Ignition` under `PROTECTIVE_FILTER_OR_GOVERNANCE` (`standalone_alpha_claim = False`).

## Verification Witness

- `python3 scripts/architecture_catalog.py && python3 scripts/architecture_catalog.py --check`, `uv run --extra dev pytest -q` (`11` passed), and `gitleaks` (`0` leaks).
