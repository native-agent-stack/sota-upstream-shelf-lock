# ADR-0025: Universal Tier-0 Full-Resolution, Always-Full-Resolution, Zero-Residual, Zero-Fallback Hard Rule

- **Status:** Accepted
- **Date:** 2026-11-20
- **Layer:** Universal Cross-Repository Merge-Gate & Manifest Enforcer (`src/shelf_lock/full_resolution_rule.py`, `scripts/merge_gate.py`, `upstream-map.toml`, `tests/test_adr0025_full_resolution_rule.py`), compounding upon `ADR-0023` and `ADR-0024` across all `18` `native-agent-stack` repos (`PROTECTIVE_FILTER_OR_GOVERNANCE`)
- **Evidence Grade:** E4 (`verify_full_resolution_manifest()` + `audit_python_text_for_empty_engine_stubs()` + `audit_repo_full_resolution()` verified directly against live `sota-compounding-lab` `ADR-0038` 9/9 full-resolution manifest SHA-256 `fcd06e224d68de521fcf6e3fc4f593a53a76d0bce311ec892b120d47aa31ccc8`, `sota-dynamic-trail-c` `ADR-0034`, exhaustive deterministic residual/fallback/post-wall rejection matrix, full `pytest`, `ruff`, `scripts/architecture_catalog.py --check`, `scripts/merge_gate.py`, `gitleaks 0`)
- **GitHub Evidence:** https://github.com/native-agent-stack/sota-upstream-shelf-lock, https://github.com/native-agent-stack/sota-compounding-lab, https://github.com/native-agent-stack/sota-dynamic-trail-c, https://github.com/nautechsystems/nautilus_trader/commit/da6b57aefdd62b44f675e434ffcfefca7f4025dd, https://github.com/nkaz001/hftbacktest/commit/5f3ec40b2afb764e0fea112f941ed85523ef4e88
- **Revisit Trigger:** Addition of a newly promoted full-resolution engine tier (e.g., real-data `Qlib` cross-sectional factor pipeline or `Databento` MBO L3 replay) to `REQUIRED_FULL_RES_ENGINES`.

## Context and Problem Statement

`ADR-0023` eliminated unmapped files and bespoke placeholders in `upstream-map.toml`, yet a forensic audit on `2026-11-20` proved that files mapped to pinned libraries could still harbor empty `BacktestEngine.run()` (`iterations=0`) boot checks, pure-Python bar-loop fallbacks labeled as `hftbacktest`, synthetic smoke tests, or silent CPU degradation. The owner established a permanent Tier-0 rule: **full resolution and always full resolution — no residual stubs or silent fallbacks anywhere in the ecosystem.**

## Decision Outcome

Add `src/shelf_lock/full_resolution_rule.py` and wire `audit_repo_full_resolution()` into `scripts/merge_gate.py` enforcing four permanent invariants:
1. **FR-1 (Zero Empty `NautilusTrader` Boot Stubs):** AST audit blocks any `BacktestEngine.run()` lacking `add_instrument`, `add_data`, and `add_strategy` (including embedded inline subprocess strings); manifest verification requires `iterations > 0`, `instruments_n >= 1`, `bars_or_ticks_loaded > 0`, `strategies_n >= 1`, `orders_total > 0`, and `fills_total > 0`.
2. **FR-2 (Zero Residual Pure-Python `hftbacktest` Loops):** Manifest verification requires `engine_kind == "RUST_HFTBACKTEST_HASHMAP_DEPTH"`, `queue_model == "RiskAdverseQueueModel"`, `slices_replayed >= 1`, and `events_replayed > 0`; residual keys like `hftbacktest_queue_parity_ref` are permanently banned.
3. **FR-3 (Zero Silent CPU / Synthetic / Post-Wall Fallbacks):** Every required engine must prove `executed=True`, `fallback_used=False`, `synthetic=False`, `degraded=False`, `post_wall_n=0`, and `rtx4090_gpu_cuda.device.startswith("cuda")`.
4. **FR-4 (Cross-Repo CLI & CI Gate):** `python -m shelf_lock.full_resolution_rule --repo <path>` audits any repository in the 18-repo fleet fail-closed.

## Alternatives Considered

1. **Allowing Optional CPU or Bar-Loop Fallbacks With Warning Logs:** Rejected unconditionally by owner Tier-0 Full-Resolution mandate.

## Consequences

- **Positive:** Guarantees that every repo, lane, and sealed manifest enforces real full-resolution upstream engine execution with zero silent degradation.
- **Negative / Safeguards:** Any stubbed engine check or degraded manifest fails `merge_gate.py` and CI immediately.

## Verification Witness

- **Live Cross-Repo Audit & Tests:** `tests/test_adr0025_full_resolution_rule.py` (exhaustive deterministic matrix across all forbidden residual keys, non-CUDA devices, `<= 0` iterations, and post-wall contamination + live `audit_repo_full_resolution(sota-compounding-lab)` returning `[]`), full `pytest`, `ruff check`, `scripts/architecture_catalog.py --check`, `scripts/merge_gate.py`, and `gitleaks 0`.
