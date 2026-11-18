# ADR-0010: Two-Stage `15s` Lit-Bid to `<= 10 bps` Marketable Collar Shelf Gate (`H095`) & `27/27` 3-Surface Parity

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

Pre-registered Trial `#94` (`H094`, `ADR-0009`) proved pure passive L1 bid resting misses `107 / 319` (`33.54%`) immediate lit breakouts (`-97.274` bps adverse selection), motivating pre-registered Trial `#95` (`H095_TWO_STAGE_LIT_QUEUE_15S_TO_10BPS_MARKETABLE_COLLAR_ORB_CPCV`, `spec_sha256 = 5abe51a4caacf4bf6955a331b495310fae1791a8d74a76c111bc9e6a35b5f4fa`, `t*(95) = 4.1858`) alongside `27/27`-runtime parity across `Mac M5 Max`, `Noesis Win32`, and `* Noesis-Carbon` `ext4`.

## Decision Outcome

1. **Publish `evaluate_two_stage_lit_to_collar_shelf_gate` (`src/shelf_lock/research_workflow.py`):**
   - Bind `hftbacktest` (`5f3ec40b2afb`, `15s` lit round-lot Stage-1 queue) to `alpaca-py` (`c42add7c0a70`) and `ib_async` (`392ad685ba04`) Stage-2 collar escalation strictly when `ask_15s_px <= initial_ask_px * 1.0010`, `0 < spread_15s_bps <= 10.0`, and `ask_15s_lots * 100 >= order_qty_shares`.
2. **Seal `10`-ADR Shelf Catalog Across the 3-Surface `27/27`-Runtime Fleet.**

## Verification Witness

- `python3 scripts/architecture_catalog.py && python3 scripts/architecture_catalog.py --check`, `uv run --extra dev pytest -q` (`9` passed), and `gitleaks protect --staged --redact --no-banner` (`0` leaks).
