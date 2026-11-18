# `sota-upstream-shelf-lock` — Immutable Upstream SHA Lock & 5-Stage Promotion Gate

Canonical public provenance & invariant verification repository for [`native-agent-stack`](https://github.com/native-agent-stack), running with **unlimited GitHub Actions CI** while keeping proprietary trading parameters and execution engines isolated in private sibling repositories.

## Capabilities
1. **18-Repo `T1–T8` Upstream Shelf Lock (`PINS_LOCK.json`):** Enforces immutable 40-character Git commit SHAs and permissive/weak-copyleft SPDX licenses across all quantitative, market-data, execution, and visualization upstreams.
2. **5-Stage Compounding Promotion Gate (`shelf_lock.validator`):** Validates promotion candidates across:
   - **Stage 1 (`SIM_EVENT_PARITY`):** `Meridian` (`nautilus_trader` + `hftbacktest` queue-fill parity)
   - **Stage 2 (`BACKTEST_PREWALL_STAT_GATE`):** Strict `<= 2026-10-15` study wall, Harvey–Liu–Zhu `t >= t*(N)` multiple-testing hurdle, native-frequency `DSR > 0.95`, `CombinatorialPurgedCV` `PBO < 0.25`, and `> 0` net 2x-cost edge
   - **Stage 3 (`PAPER_24X5_EXECUTION`):** `ADR-0022 <= 2.00%` protective stops, `<= 200 req/min` Alpaca Paper + `<= 3,000 msg/min` IBKR (`:4002`) pacing, and live-account hard refusal
   - **Stage 4 (`EMPIRICAL_BAYES_FINETUNE`):** `n_closed >= 30` realized paper fills + pre-registered regime split (`Dec 6, 2026` `23/5 SIP`)
   - **Stage 5 (`BROKER_PROMOTION_READINESS`):** Owner-gated Alpaca / IBKR promotion readiness manifest
3. **MADR 4.0 Architecture Catalog (`docs/adr/CATALOG.md`):** Verified for zero drift on every push, PR, and daily scheduled GitHub Action.

## Quick Verification
```bash
pytest -v
python scripts/architecture_catalog.py --check
PYTHONPATH=src python -m shelf_lock.validator --verify-no-leaks
```
