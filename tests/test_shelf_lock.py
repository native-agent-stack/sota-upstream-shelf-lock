from __future__ import annotations

import json
import pathlib
import subprocess
import sys

from shelf_lock import (
    PromotionCandidate,
    compute_hlz_t_hurdle,
    load_pins_lock,
    scan_repo_privacy_hygiene,
    validate_pins_lock,
    validate_promotion_candidate,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_pins_lock_18_upstreams_and_invariants() -> None:
    doc = load_pins_lock(REPO_ROOT)
    assert validate_pins_lock(doc, online_ls_remote=False) == []
    assert len(doc["upstreamShelfPins"]) == 18
    assert [s["stage"] for s in doc["compoundingPipelineStages"]] == [1, 2, 3, 4, 5]


def test_hlz_multiple_testing_hurdle_monotone() -> None:
    t1 = compute_hlz_t_hurdle(1)
    t78 = compute_hlz_t_hurdle(78)
    t83 = compute_hlz_t_hurdle(83)
    assert t1 == 3.00
    assert 4.13 < t78 < t83 < 4.25


def test_five_stage_promotion_gate_enforces_all_invariants() -> None:
    passing = PromotionCandidate(
        strategy_id="H07_PASSIVE_QUEUE_ATR_TRAIL",
        calibration_max_date="2026-10-15",
        cumulative_trials_n=83,
        clustered_t_stat=4.42,
        dsr_probability=0.985,
        cpcv_pbo=0.12,
        net_2x_cost_bps=14.5,
        max_protective_stop_pct=1.60,
        paper_closed_trades=42,
        alpaca_orders_per_min_cap=200,
        uses_live_host_or_port=False,
    )
    ok, reasons = validate_promotion_candidate(passing)
    assert ok is True and reasons == []

    failing = PromotionCandidate(
        strategy_id="LEAKY_AND_UNSAFE",
        calibration_max_date="2026-10-16",
        cumulative_trials_n=83,
        clustered_t_stat=2.10,
        dsr_probability=0.60,
        cpcv_pbo=0.45,
        net_2x_cost_bps=-5.6,
        max_protective_stop_pct=2.50,
        paper_closed_trades=12,
        alpaca_orders_per_min_cap=1000,
        uses_live_host_or_port=True,
    )
    ok_bad, bad_reasons = validate_promotion_candidate(failing)
    assert ok_bad is False
    assert len(bad_reasons) == 9


def test_adr_catalog_zero_drift_and_privacy_hygiene() -> None:
    res = subprocess.run(
        [sys.executable, "scripts/architecture_catalog.py", "--check"],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert scan_repo_privacy_hygiene(REPO_ROOT) == []


def test_starred_convergence_catalog_v3108() -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "STARRED_CONVERGENCE_CATALOG.json").read_text(encoding="utf-8"))
    pins_doc = load_pins_lock(root)

    assert catalog["schemaVersion"] == "sota-starred-convergence.v3.10.8"
    assert catalog["verifiedDate"] == "2026-11-19"
    assert catalog["ownerStarredTotalAudited"] == 415
    assert catalog["beyondStarredTotal"] == 8
    assert catalog["authority"] == "PHILOSOPHY_ONLY"
    assert catalog["immutableCorePinsPreserved"] == len(pins_doc["upstreamShelfPins"]) == 18

    redteam_repos = {item["repo"] for item in catalog["redteam_and_security"]}
    assert {
        "elementalsouls/Claude-BugHunter",
        "cloudflare/security-audit-skill",
        "NVIDIA/OpenShell",
        "trailofbits/skills",
        "morluto/rea",
    } <= redteam_repos

    eval_repos = {item["repo"] for item in catalog["skill_eval_and_agent_quality"]}
    assert {"NVIDIA/SkillEvaluator", "Nutlope/hallmark", "meta/astryx"} <= eval_repos

    orch_repos = {item["repo"] for item in catalog["multi_runtime_orchestration_and_loops"]}
    assert {
        "Tencent/LoopForge",
        "backnotprop/plannotator",
        "rlaope/oh-my-hermes",
        "alvinunreal/oh-my-opencode-slim",
        "mvschwarz/openrig",
    } <= orch_repos

    ontology_repos = {item["repo"] for item in catalog["ontology_search_and_context"]}
    assert {"NVIDIA/auto-ontology", "xerj-org/xerj", "opendatalab/MinerU"} <= ontology_repos

    quant_repos = {item["repo"] for item in catalog["quant_trading_and_microstructure"]}
    assert {
        "microsoft/qlib",
        "openbq-org/OpenBB",
        "tradermonty/claude-trading-skills",
        "TraderAlice/OpenAlice",
    } <= quant_repos

    beyond = catalog["beyond_starred_sota_additions"]
    assert len(beyond) == 8
    beyond_repos = {item["repo"] for item in beyond}
    assert {
        "microsoft/RD-Agent",
        "databento/databento-python",
        "stanfordnlp/dspy",
        "microsoft/SkillOpt",
    } <= beyond_repos


def test_landscape_release_audit_20261119_and_immutable_pins() -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "STARRED_CONVERGENCE_CATALOG.json").read_text(encoding="utf-8"))
    pins_doc = load_pins_lock(root)

    assert len(pins_doc["upstreamShelfPins"]) == 18
    audit = catalog["landscapeReleaseAudit20261119"]
    assert audit["authority"] == "PHILOSOPHY_ONLY_AND_HOST_VERSIONS"
    entries = audit["entries"]
    assert entries["stablyai/orca"]["installed"] == "1.4.263"
    assert entries["stablyai/orca"]["latest"] == "v1.4.264"
    assert entries["anthropics/claude-code"]["installed"] == "2.1.328"
    assert entries["google-antigravity"]["installed"] == "1.5.12"
    assert entries["can1357/oh-my-pi"]["latest"] == "v19.0.0"
    assert entries["code-yeongyu/oh-my-openagent"]["latest"] == "v5.1.79"
    assert entries["openai/codex"]["latest"] == "rust-v0.170.0"
