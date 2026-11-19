# ADR-0016: `v3.10.9` Nov 19 Upstream Landscape Release Audit & Dual-Machine Orca Manifest Parity

- **Status:** Accepted
- **Date:** 2026-11-19
- **Evidence Grade:** E4

## Context and Problem Statement

Live GitHub release and local CLI telemetry on `2026-11-19` showed multiple orchestrator and runtime updates across our starred and pinned ecosystem: `stablyai/orca` (`v1.4.263` active on Win32 & Mac, `v1.4.264` released today), `anthropics/claude-code` (`v2.1.328` live), `google-antigravity` (`1.5.12` live), `can1357/oh-my-pi` (`v19.0.0`), `code-yeongyu/oh-my-openagent` (`v5.1.79`), `openai/codex` (`rust-v0.170.0`), `Yeachan-Heo/oh-my-codex` (`v0.22.11`), `backnotprop/plannotator` (`v0.29.0`), `mvschwarz/openrig` (`v0.7.19`), `NVIDIA/SkillEvaluator` (`v1.0.1`), and `astral-sh/uv` (`0.13.9`), alongside the `Noesis` RTX 4090 `:8794` CUDA sidecar (`ADR-0036`) and `18/18` `sota-doctor` checks. We need an auditable `PHILOSOPHY_ONLY_AND_HOST_VERSIONS` record without mutating the `18` frozen `40`-char quantitative `PINS_LOCK.json` SHAs.

## Decision Outcome

1. **Publish `landscapeReleaseAudit20261119` in `STARRED_CONVERGENCE_CATALOG.json`:** Capture installed/pinned versions versus latest upstream releases across the `11` key orchestration/CLI tools while preserving all `415` audited stars, `8` beyond-starred frameworks, and `18` immutable `PINS_LOCK.json` SHAs.
2. **Update `UPSTREAM.md` (`v3.10.9`):** Synchronize Section 1 to `claude-code v2.1.328`, `agy 1.5.12`, `stablyai/orca 1.4.263` live / `v1.4.264` evaluated, `9/9` 3-surface Orca lane hubs, `17/17` live dual-machine Orca automations, `:8794` RTX 4090 CUDA sidecar, and `18/18` `sota-doctor`.
3. **Add Automated Catalog Parity Tests:** Validate `landscapeReleaseAudit20261119` and `18/18` preserved pins inside `tests/test_shelf_lock.py`.

## Verification Witness

- `uv run python scripts/architecture_catalog.py` & `--check` (`16` ADRs valid, `0` drift), `uv run ruff format --check .`, `uv run ruff check .`, `uv run --extra dev pytest -v`, `uv run python -m shelf_lock.validator --verify-no-leaks`, and `gitleaks git --staged --verbose` (`0` leaks).
