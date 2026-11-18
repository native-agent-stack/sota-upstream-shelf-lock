# ADR-0011: `v3.9.8` `Trial #96` (`H096`) Pure Dry-Powder `15s` Bid-Survival & Informed-Flow Joint Collar Gate

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

Pre-registered Trial `#95` (`H095`, `ADR-0010`) revealed that posting a resting passive L1 bid during `[0..15s]` suffers `-8.736` bps net `1x` (`59.7%` `trade_through` sweeps), whereas pre-registered Trial `#96` (`H096_DRY_POWDER_15S_BID_SURVIVAL_10BPS_COLLAR_ORB_CPCV`, `spec_sha256 = 588d27755badb38da2ebe7a762c8106b210a0333842b0a58d0724531583fbb5f`, `N = 96 -> t*(97) = 4.1905`) proved the `+29.564` bps joint necessity of informed flow (`OFI >= 0.25` and `ISO_F >= 0.15 | BJZZ >= 0.12`) AND pure dry-powder `15s` bid-survival (`0` resting orders in `(0, 15s]`, `min_lit_roundlot_px >= initial_bid_px`, `bid_15s_px >= initial_bid_px`): the wide `OFI > 0` cohort bled `-12.729` bps net `1x` (`t = -0.7781`, `FAILED` on `ALPHA_STRATEGY_MINOR`), while the strict informed-flow + `15s` dry-powder collar cohort (`n = 52` / `47` dates) earned `+16.835` bps net `1x` / `+11.366` bps net `2x` (`11/15 = 73.33%` disjoint CPCV `> 0`, `3/3` years positive at `2x`).

## Decision Outcome

1. **Publish `evaluate_dry_powder_15s_bid_survival_collar_gate` (`src/shelf_lock/research_workflow.py`):**
   - Require `resting_orders_0_15s == 0`, `ofi_entry >= 0.25` with `(iso_f_buy_share >= 0.15 or bjzz_inst_dark_share >= 0.12)`, `min_lit_roundlot_px_0_15s >= initial_bid_px`, `bid_15s_px >= initial_bid_px`, and `evaluate_two_stage_lit_to_collar_shelf_gate` approval (`<= 10.0` bps collar & ask depth) under `PROTECTIVE_FILTER_OR_GOVERNANCE` (`standalone_alpha_claim = False`).

## Verification Witness

- `python3 scripts/architecture_catalog.py && python3 scripts/architecture_catalog.py --check`, `uv run --extra dev pytest -q` (`10` passed), and `gitleaks` (`0` leaks).
