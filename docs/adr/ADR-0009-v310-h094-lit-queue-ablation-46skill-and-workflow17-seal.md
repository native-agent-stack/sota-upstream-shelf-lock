# ADR-0009: v3.10.0 Controlled `H094` Lit-Queue Shelf Ablation, `46`-Skill Parity & Workflow `#17` Seal

- **Status:** Accepted
- **Date:** 2026-11-18
- **Evidence Grade:** E4

## Context and Problem Statement

Following `ADR-0008`, pre-registered Trial `#94` (`H094_LIT_ROUNDLOT_STRICT_10BPS_20M_HIGH_OFI_NO_REGSHO_ORB_CPCV`, `spec_sha256 = 5f039dc14ab73d44c8d7d28b116782b0d08f686b7580140c7e8724efa1313bc4`, `t*(94) = 4.1834`) executed a controlled single-factor ablation across `11,652` pre-wall ORB files (`<= 2026-10-15`, `56` workers on `Noesis` `Z:/sota-data/prewall-lake`) using pinned `hftbacktest` (`5f3ec40b2afb`), `skfolio` (`eb97978f73f1`), `ml4t-diagnostic` (`19e76072e64a`), `polars` (`7f9ff152f095`), and `edgartools` (`574c2bd15f6c`), alongside the `v3.10.0` `46`-skill cross-harness enactor (`~/.agents/bin/sota-workflow`, Workflow `#17`).

## Decision Outcome

1. **Seal the `18`-Pin Shelf (`cb34b0c35043...`) Against the `H090` / `H091` / `H094` Empirical Triad (`N = 94`, `t*(95) = 4.1858`):**
   - Tightening `H091` (`<= 12.0` bps, `ADV_20d >= $10M`, `OFI >= 0.15`: `-23.732` bps net `1x`) back to `H090`'s strict `<= 10.0` bps / `ADV_20d >= $20M` / `OFI >= 0.25` envelope under identical strict lit round-lot queue depletion (`x != 'D'`, non-`'I'`, `s >= 100`) lifted `net_return_1x_bps` by **`+25.886` bps** to **`+2.154` bps** (`212 / 319 = 66.46%` fills across `175` dates, `+7.542` bps gross excess, `7/15` positive `C(6,2)` disjoint split OOS Sharpes), validating `sota-mover-ranker` `ADR-0017`/`ADR-0019` protective bounds.
   - Simultaneously, excluding off-exchange TRF (`x == 'D'`) and odd-lot (`'I'`, `s < 100`) queue leakage exposed `-97.274` bps runaway adverse selection (`107` immediate breakouts unfilled; `-3.233` bps at `2x`, `t = 0.1374 < 4.1834`, **FAILED** on `ALPHA_STRATEGY_MINOR`), proving pure passive L1 bid resting requires marketable `<= 10.0` bps collar execution on directional ignitions.
2. **Bind `sota-upstream-shelf-lock` (`9` ADRs) to `v3.10.0` `46`-Skill & `17`-Workflow Parity.**

## Verification Witness

- `python3 scripts/architecture_catalog.py --write && python3 scripts/architecture_catalog.py --check`, `uv run --extra dev pytest -q`, and `gitleaks protect --staged --redact --no-banner` (`0` leaks).
