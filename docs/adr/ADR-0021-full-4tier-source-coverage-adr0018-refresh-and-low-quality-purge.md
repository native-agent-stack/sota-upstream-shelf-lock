# ADR-0021: Full 4-Tier SOTA Source Coverage (Official, Upstream, Community & Beyond), `ADR-0018` Security/License Refresh, `NCSA`/`BSD-2-Clause` Validator Expansion & Low-Quality Source Purge

- **Status:** Accepted
- **Date:** 2026-11-20
- **Evidence Grade:** E4 (`STARRED_CONVERGENCE_CATALOG.json`, `src/shelf_lock/validator.py`, `tests/test_adr0021_full_source_coverage.py`, `tests/test_shelf_lock.py`, `50/50` live GitHub API stars + 40-char HEAD SHAs verified `2026-11-20`, `scripts/architecture_catalog.py --check`, `pytest`, `ruff`, `ty` `0` diagnostics, `gitleaks 0`)
- **GitHub Evidence:** https://github.com/bashtage/arch/commit/d3e858fc1c99932bb6936cbaf0d1b45b136266e5, https://github.com/openbq-org/OpenBB/commit/5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0, https://github.com/openbq-org/backends-for-openbb/commit/a6293707576e16edda8305adda95b07b6a4b968b, https://github.com/microsoft/qlib/commit/54355232463878d2eebb91fe0ee5fa7fa1f5976c, https://github.com/lballabio/QuantLib/commit/8c52b45180d074d899a94f990140cba5b425f2d8, https://github.com/goldmansachs/gs-quant/commit/70220e300524d54bd273be0f4c485d53b3780482, https://github.com/questdb/questdb/commit/9a9388714bd4b3b7ee8887f09dbdc229423baef9

## Context and Problem Statement

Following `ADR-0020`, three remaining governance gaps existed across the upstream shelf and ecosystem source coverage:
1. `src/shelf_lock/validator.py::ALLOWED_LICENSES` lacked OSI-permissive `NCSA` (`bashtage/arch`, `bashtage/linearmodels`) and `BSD-2-Clause` (`ib-api-reloaded/ib_async`, `deepcharles/ruptures`), leaving avoidable license-exception technical debt.
2. Full 4-tier source coverage — **Official/Regulatory/Exchange**, **18 Immutable Core Upstreams**, **18 Frontier OSS Libraries**, and **19 Official/Foundation/Institutional/Community/Beyond Repositories** — needed unified 40-char SHA provenance, live GitHub star synchronization (`50/50` newly starred on `seathatflowsinourveins` so all `18` core + `18` frontier + `19` official/community/beyond repos are starred), refreshed `ADR-0018` security/license pointers (`qlib v0.9.8`, `openbq-org/backends-for-openbb`, `openbq-org/OpenBB openbb-v5.0.0` `Apache-2.0`), and an explicit **15-item Low-Quality / Non-Permissive / Scraper Purge Denylist**.
3. `tests/test_shelf_lock.py` carried `34` `ty` type-checker diagnostics from untyped `**dict` unpacking into `PromotionCandidate`.

## Decision Outcome

1. **Expand `ALLOWED_LICENSES` (`src/shelf_lock/validator.py`):** Add OSI-approved permissive `NCSA` and `BSD-2-Clause` alongside `MIT`, `Apache-2.0`, `BSD-3-Clause`, and `LGPL-3.0-or-later` (copyleft `GPL`/`AGPL`, `BUSL-1.1`, `Commons Clause`, `Proprietary`, and non-commercial weight licenses remain 100% blocked).
2. **Add `fullSourceCoverageAndStarredManifest` (`schemaId: sota-v3114-full-source-coverage-and-cleanup.v1`)** to `STARRED_CONVERGENCE_CATALOG.json`:
   - Preserves all **18 immutable core pins in `PINS_LOCK.json`** byte-for-byte (`SHA-256` verified).
   - Seals all **7 Official/Regulatory/Exchange primary sources**, **19 Official/Foundation/Institutional/Community/Beyond starred repositories** (verified 40-char SHAs & SPDX licenses), refreshed **`ADR-0018` pointers**, live **`50/50` GitHub Star Sync Receipt**, and **15 purged low-quality/copyleft/scraper sources**.
3. **Zero `ty` Diagnostics Cleanup:** Refactor `test_adr0017_promotion_boundary_hlz_dsr_pbo` in `tests/test_shelf_lock.py` to use typed `PromotionCandidate` + `dataclasses.replace`, eliminating all `34` pre-existing `ty` diagnostics across the repository.
4. **Zero Trial Consumption & Paper-Only Firewall:** Ships strictly as `PROTECTIVE_FILTER_OR_GOVERNANCE` (`standaloneAlphaClaim = false`, `hlzTrialConsumed = false`, preserving `Trial #105` `t*(105) = 4.2084`).

## Alternatives Considered

- **Mutate historical `ADR-0018` JSON fields in place:** Rejected — preserves full audit traceability of `ADR-0018` regression tests while providing authoritative refreshed pointers in `ADR-0021`.
- **Keep `yfinance`, `backtrader`, `timesfm v3.0 weights`, or `AGPL`/`GPL` quant tools in active research adapters:** Rejected — violates institutional PIT data integrity and OSI-permissive license hygiene.

## Verification Witness

- `scripts/architecture_catalog.py --check` (`21/21` ADRs, `0` drift), `pytest -q` (incl. `tests/test_adr0021_full_source_coverage.py`), `ruff check .`, `ruff format --check .`, `ty check` (`0` diagnostics across the entire repo), and `gitleaks protect --staged --no-banner` (`0` leaks).

## Rollback

Revert the single `ADR-0021` commit; `PINS_LOCK.json` and `ADR-0001..0020` remain untouched.
