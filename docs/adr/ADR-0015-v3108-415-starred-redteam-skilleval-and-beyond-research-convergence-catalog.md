# ADR-0015: `v3.10.8` 415-Starred, Red-Team, SkillEvaluator & Beyond-Starred Convergence Catalog

- **Status:** Accepted
- **Date:** 2026-11-19
- **Evidence Grade:** E4

## Context and Problem Statement

Owner GitHub stars reached `415` repositories on `2026-11-19`, introducing frontier Red-Team (`elementalsouls/Claude-BugHunter`, `cloudflare/security-audit-skill`, `NVIDIA/OpenShell`, `morluto/rea`), 4-tier Skill Quality (`NVIDIA/SkillEvaluator`), scripted agent convergence (`Tencent/LoopForge`, `backnotprop/plannotator`, `rlaope/oh-my-hermes`, `alvinunreal/oh-my-opencode-slim`, `mvschwarz/openrig`), ontology/retrieval (`NVIDIA/auto-ontology`, `xerj-org/xerj`, `opendatalab/MinerU`), and UI craft (`Nutlope/hallmark`, `meta/astryx`), alongside `8` beyond-starred foundations (`microsoft/RD-Agent`, `databento/databento-python`, `unit8co/darts`, `Nixtla/statsforecast`, `stanfordnlp/dspy`, `adia-lab-19-mintrl`, `mlfinlab-triple-barrier`, `microsoft/SkillOpt`). Without a structured machine-readable catalog under `PHILOSOPHY_ONLY` authority (`ADR-0001`/`ADR-0004`), downstream harnesses risk either missing newly starred capabilities or confusing distilled workflow patterns with the `18` immutable `40`-char pinned execution/research libraries in `PINS_LOCK.json`.

## Decision Outcome

1. **Publish `STARRED_CONVERGENCE_CATALOG.json` (`v3.10.8`):** Group the verified `415` owner-starred frontier anchors (`redteam_and_security`, `skill_eval_and_agent_quality`, `multi_runtime_orchestration_and_loops`, `ontology_search_and_context`, `quant_trading_and_microstructure`) and `8` `beyond_starred_sota_additions` under strict `authority: "PHILOSOPHY_ONLY"`, preserving zero local home paths and zero broker account IDs.
2. **Preserve `18/18` Immutable `40`-Char `PINS_LOCK.json` SHAs:** Advance `PINS_LOCK.json` `verifiedDate` to `2026-11-19` while keeping all `18` upstream SHA pins bit-exact for deterministic `RiskAdverseQueueModel` and pre-wall (`<= 2026-10-15`) reproducibility.
3. **Update `UPSTREAM.md` (`v3.10.8`) & Add Catalog Invariant Tests:** Align Section 1 to `stablyai/orca v1.4.263`, `60` canonical skills, `21` workflows, `15/15` dual-machine automations, and `415+8` starred convergence, and validate catalog invariants inside `tests/test_shelf_lock.py`.

## Verification Witness

- `uv run python scripts/architecture_catalog.py` & `--check` (`15` ADRs, `0` drift), `uv run ruff format --check .`, `uv run ruff check .`, `uv run pytest -v`, `uv run python -m shelf_lock.validator --verify-no-leaks`, and `gitleaks git --staged --verbose` (`0` leaks).
