# ADR-0018: v3.11.0 Upstream-First Pinning of `microsoft/qlib` (`Alpha158` Benchmark) & `OpenBB-finance/backends-for-openbb` Workspace Backend Protocol

- **Status:** Accepted
- **Date:** 2026-11-20
- **Evidence Grade:** E4
- **GitHub Evidence:** https://github.com/microsoft/qlib/commit/da920b7f954f48ab1bb64117c976710de198373e, https://github.com/microsoft/qlib/commit/54355232463878d2eebb91fe0ee5fa7fa1f5976c, https://github.com/OpenBB-finance/backends-for-openbb/commit/a6293707576e16edda8305adda95b07b6a4b968b, https://github.com/OpenBB-finance/OpenBB/commit/dddc3b328284bb953b6e5468b167b39c78490001

## Context and Problem Statement

The `v3.11.0` wave retires static generated Pine tables (`/api/pine/live_ranker`), deprecates hand-rolled HTML cockpits in favor of an upstream-first `OpenBB Workspace` custom backend (`ADR-0062`), and introduces a pre-wall (`<= 2026-10-15`) cross-sectional `Alpha158` / `LightGBM` market-neutral benchmark inside the `S1` Alpha Factory (`ADR-0064` / `sota-compounding-lab ADR-0027`). Per `ADR-0001` and `ADR-0017`, the 18 immutable core shelf clones in `~/Documents/upstream/` and `PINS_LOCK.json` must remain untouched, while new upstream evaluations and protocol pins must be recorded with verified 40-char commit SHAs and SPDX licenses.

## Decision Outcome

1. **Preserve all 18 immutable `PINS_LOCK.json` core pins untouched** (`immutableCorePinsUntouched = 18`) and preserve `ADR-0017`'s `terminalPlatformTaxonomy` block byte-for-byte.
2. **Add additive `alphaFactoryAndTerminalExtensions` block (`schemaId: sota-v3110-alpha-terminal-extensions.v1`)** in `STARRED_CONVERGENCE_CATALOG.json`:
   - **`microsoft/qlib`** (`MIT`, tag `v0.9.7` @ `da920b7f954f48ab1bb64117c976710de198373e`, `main` @ `54355232463878d2eebb91fe0ee5fa7fa1f5976c`): evaluated & pinned as the `Alpha158` / `LightGBM` cross-sectional market-neutral benchmark for `S1` pre-wall (`<= 2026-10-15`) CPCV/DSR/HLZ sweeps. Carries zero order authority (`orderAuthority = false`).
   - **`OpenBB-finance/backends-for-openbb`** (`MIT`, `main` @ `a6293707576e16edda8305adda95b07b6a4b968b`): pinned as the upstream-first FastAPI custom backend SDK protocol (`widgets.json`, `apps.json`, CORS `https://pro.openbb.co`), paired with companion platform `OpenBB-finance/OpenBB` (`v4.7.0` @ `dddc3b328284bb953b6e5468b167b39c78490001`, `AGPL-3.0-only`, `OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH_NON_BUNDLED`). Live broker ports (`4001`, `7496`, `8796`, `8798`) and hosts (`api.alpaca.markets`) remain 100% hard-refused.
3. **Zero alpha-promotion elevation:** This pin adds research benchmarking and terminal visualization/paper-staging contracts only (`PROTECTIVE_FILTER_OR_GOVERNANCE`).

## Alternatives Considered

- **Mutate `~/Documents/upstream/` clones or expand `PINS_LOCK.json` beyond 18 core entries:** Rejected; breaks `ADR-0001` immutability invariants and downstream `18`-pin hash parity across 18 repos.
- **Embed OpenBB platform AGPL/non-SPDX code into core execution:** Rejected; cleanly decouples via the MIT `backends-for-openbb` HTTP JSON/FastAPI widget protocol over loopback.

## Verification Witness

- Live `git ls-remote` & `gh api` verified on `2026-11-20`: `microsoft/qlib` (`MIT`, `v0.9.7` `da920b7f954f48ab1bb64117c976710de198373e`), `OpenBB-finance/backends-for-openbb` (`MIT`, `HEAD` `a6293707576e16edda8305adda95b07b6a4b968b`), `OpenBB-finance/OpenBB` (`AGPL-3.0-only`, `v4.7.0` `dddc3b328284bb953b6e5468b167b39c78490001`, non-bundled).
- Enforced by `tests/test_shelf_lock.py::test_adr0018_v3110_qlib_and_openbb_extensions`, `scripts/architecture_catalog.py --check`, `ruff`, and `gitleaks`.

## Rollback

Revert the single commit adding `alphaFactoryAndTerminalExtensions` and `ADR-0018`; all 18 core pins and `ADR-0017` remain unchanged.
