# ADR-0024: Clean-Room Sim->Paper->Live Org Blueprint & Full 18/18 Workstation Hard-Rule Enforcement

- **Status:** Accepted
- **Date:** 2026-11-20
- **Builds Upon:** `ADR-0023` (`hard_upstream_rule.py`)

## Context
The owner mandated that every single line across the entire ecosystem — repositories, ADRs, sealed manifests, hooks, skills, backtest platforms, strategies, and Orca workflows — must originate from pinned SOTA upstream sources, with research convergence first and clean Sim->Paper->Live separation (including the ability to spin out a clean-room Sim->Paper->Live GitHub org if ever needed).

## Decision
1. Extend `shelf_lock.hard_upstream_rule.parse_upstream_md_components()` to parse multi-column layer tables (`| **L0** | \`comp\` |`) and GitHub repository URLs across all 18 `native-agent-stack` repos cleanly.
2. Add `--require-full-compliance` to `--audit-workstation` so CI and Orca automations fail closed unless `100%` (`18/18`) of repositories pass `UPSTREAM.md`, `upstream-map.toml`, ADR evidence, and 18-pin shelf parity.
3. Add `bootstrap_cleanroom_spl_org()` (`--bootstrap-org-blueprint <dir>`) generating a turnkey 6-repo Sim->Paper->Live clean-room organization pre-wired with `UPSTREAM.md`, `upstream-map.toml`, fail-closed `scripts/merge_gate.py`, `ADR-0001`, `orca.yaml`, and SHA-256 `ORG_BLUEPRINT_MANIFEST.json`.

## Verification & Evidence
- Verified locally with `pytest -q` (including clean-room org bootstrapper & `--require-full-compliance` unit tests), `ruff check .`, `scripts/merge_gate.py` (`[MERGE-GATE PASS]`), and `gitleaks protect --staged --no-banner` (`0` leaks).
