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
from shelf_lock.validator import ALLOWED_LICENSES

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


TAXONOMY_CLASSES = [
    "PINNED_INTEGRATE",
    "PHILOSOPHY_ONLY",
    "OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH",
    "HARD_REFUSED_EXECUTION_SAAS",
]
TAXONOMY_SURFACES = {
    "perspective": "PINNED_INTEGRATE",
    "lightweight-charts": "PINNED_INTEGRATE",
    "nautilus_trader": "PINNED_INTEGRATE",
    "hftbacktest": "PINNED_INTEGRATE",
    "TrendSpider": "PHILOSOPHY_ONLY",
    "Bookmap": "PHILOSOPHY_ONLY",
    "Sierra Chart": "PHILOSOPHY_ONLY",
    "DAS Trader Pro": "PHILOSOPHY_ONLY",
    "QuantConnect / LEAN": "PHILOSOPHY_ONLY",
    "FinceptTerminal": "PHILOSOPHY_ONLY",
    "Flowsurface": "PHILOSOPHY_ONLY",
    "TradingView Desktop": "OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH",
    "OpenBB Platform / Workspace": "OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH",
    "SignalStack": "HARD_REFUSED_EXECUTION_SAAS",
}
EXISTING_ANCHOR_GROUPS = (
    "redteam_and_security",
    "skill_eval_and_agent_quality",
    "multi_runtime_orchestration_and_loops",
    "ontology_search_and_context",
    "quant_trading_and_microstructure",
    "beyond_starred_sota_additions",
)


def _load_catalog_and_pins() -> tuple[dict, dict]:
    catalog = json.loads((REPO_ROOT / "STARRED_CONVERGENCE_CATALOG.json").read_text(encoding="utf-8"))
    return catalog, load_pins_lock(REPO_ROOT)


def test_adr0017_terminal_platform_taxonomy_classes_and_14_surfaces() -> None:
    catalog, pins_doc = _load_catalog_and_pins()
    taxonomy = catalog["terminalPlatformTaxonomy"]

    assert taxonomy["schemaId"] == "sota-terminal-platform-taxonomy.v1"
    assert taxonomy["adr"] == "ADR-0017"
    assert taxonomy["classes"] == TAXONOMY_CLASSES
    assert set(taxonomy["classPredicates"]) == set(TAXONOMY_CLASSES)

    rows = taxonomy["namedSurfaces"]
    assert taxonomy["namedSurfacesCount"] == len(rows) == 14
    assert {r["surface"]: r["class"] for r in rows} == TAXONOMY_SURFACES
    assert all(r["orderAuthority"] is False for r in rows)

    pins = {p["name"]: p for p in pins_doc["upstreamShelfPins"]}
    assert len(pins) == 18
    pinned_rows = [r for r in rows if r["class"] == "PINNED_INTEGRATE"]
    assert len(pinned_rows) == 4
    for row in pinned_rows:
        pin = pins[row["pinName"]]
        assert row["surface"] == pin["name"]
        assert row["commit"] == pin["commit"] and len(row["commit"]) == 40
        assert all(c in "0123456789abcdef" for c in row["commit"])
        assert (row["url"], row["ref"], row["license"]) == (pin["url"], pin["ref"], pin["license"])
    named_pins = {r["pinName"] for r in pinned_rows}
    others = taxonomy["pinnedIntegrateOtherShelfPins"]
    assert len(others) == 14 and named_pins.isdisjoint(others)
    assert named_pins | set(others) == set(pins)

    pin_names_lower = {name.lower() for name in pins}
    for row in rows:
        if row["class"] != "PINNED_INTEGRATE":
            assert row["surface"].lower() not in pin_names_lower
        if row["class"] == "PHILOSOPHY_ONLY":
            assert row["runtimeImport"] is False and row["lockfileEntry"] is False
            assert row["account"] is False and row["feed"] is False
        if row["class"] == "OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH":
            assert row["coreAuthority"] == "PHILOSOPHY_ONLY"
            assert row["importedByCore"] is False and row["coreTestsPassWhenAbsent"] is True
        if row.get("closedSource"):
            assert not any(k in row for k in ("version", "ref", "commit"))

    fincept = next(r for r in rows if r["surface"] == "FinceptTerminal")
    assert fincept["class"] == "PHILOSOPHY_ONLY"
    assert fincept["license"] == "AGPL-3.0" and fincept["licenseAllowedForPin"] is False
    assert "AGPL-3.0" not in ALLOWED_LICENSES

    openbb = next(r for r in rows if r["surface"] == "OpenBB Platform / Workspace")
    assert openbb["catalogAnchor"] == "openbq-org/OpenBB"

    refused = {r["route"] for r in taxonomy["hardRefusedRoutes"]}
    assert {
        "SignalStack alert-to-broker relay",
        "TrendSpider + SignalStack relay",
        "TradingView alert-to-webhook order bridges",
        "Unguarded chart-click orders",
        "Closed SaaS execution relays",
        "QuantConnect cloud live deployment",
    } <= refused
    assert taxonomy["visualArtifactsMayBindAlertOrWebhook"] is False
    assert all(p["paperOnly"] is True for p in taxonomy["firstPartyPaperPathsOutsideTaxonomy"])


def test_adr0017_dual_asset_provenance_and_disjoint_ports() -> None:
    catalog, pins_doc = _load_catalog_and_pins()
    taxonomy = catalog["terminalPlatformTaxonomy"]
    pins = {p["name"]: p for p in pins_doc["upstreamShelfPins"]}

    chart = taxonomy["chartAssetProvenance"]
    assert chart["shelfCommit"] == pins["lightweight-charts"]["commit"]
    assert chart["shelfCommit"] == "c29c51e1e5bc61981da5832c97797cb8283d120f"
    assert chart["shelfPackageVersion"] == "5.3.0"
    assert chart["deployedVersion"] == "5.0.8"
    assert chart["deployedReleaseCommit"] == "c65d0697ad0c546301a1734912ca50d031d468a2"
    assert chart["deployedAssetSha256"] == "bcdca2a528db7c9b386918c99c544bde3eda3f0204ec2d23a64411d4cb4686c9"

    persp = taxonomy["perspectiveProvenance"]
    assert persp["pinsLockUrl"] == pins["perspective"]["url"] == "https://github.com/finos/perspective"
    assert persp["pinsLockCommit"] == pins["perspective"]["commit"]
    assert persp["pinsLockRef"] == pins["perspective"]["ref"] == "v5.9.2"
    assert persp["workflowsAdr0035Repo"] == "perspective-dev/perspective"
    assert persp["runtimeNpmScope"] == "@perspective-dev"
    assert persp["runtimeNpmVersion"] == "5.9.2"

    paper = taxonomy["loopbackPaperPorts"]
    live = taxonomy["forbiddenLivePorts"]
    assert paper == [4002, 8787, 8797, 8799]
    assert live == [4001, 7496, 8796, 8798]
    assert set(paper).isdisjoint(live)
    invariants = pins_doc["invariants"]
    assert set(invariants["forbiddenLivePorts"]) <= set(live)
    assert invariants["ibkrPaperPort"] in paper
    ref_file, pointer = taxonomy["forbiddenLiveHostsRef"].split("#")
    assert ref_file == "PINS_LOCK.json" and pointer == "/invariants/forbiddenLiveHosts"
    assert invariants["forbiddenLiveHosts"] == ["api.alpaca.markets"]


def test_adr0017_no_existing_anchor_or_pin_regression() -> None:
    catalog, pins_doc = _load_catalog_and_pins()

    assert catalog["schemaVersion"] == "sota-starred-convergence.v3.10.8"
    assert catalog["authority"] == "PHILOSOPHY_ONLY"
    assert catalog["ownerStarredTotalAudited"] == 415
    assert catalog["beyondStarredTotal"] == 8
    assert catalog["immutableCorePinsPreserved"] == len(pins_doc["upstreamShelfPins"]) == 18
    assert len(catalog["beyond_starred_sota_additions"]) == 8
    for group in EXISTING_ANCHOR_GROUPS:
        assert all(item["authority"] == "PHILOSOPHY_ONLY" for item in catalog[group]), group
    quant_repos = {item["repo"] for item in catalog["quant_trading_and_microstructure"]}
    assert "openbq-org/OpenBB" in quant_repos


def test_adr0017_promotion_boundary_hlz_dsr_pbo() -> None:
    catalog, _ = _load_catalog_and_pins()
    boundary = catalog["terminalPlatformTaxonomy"]["promotionBoundary"]
    assert boundary["taxonomyGrantsStageElevation"] is False
    assert boundary["hlzCallingConvention"] == "candidate-inclusive"
    assert boundary["completedLedgerTrials"] + 1 == boundary["cumulativeTrialsN"] == 104
    assert compute_hlz_t_hurdle(104) == boundary["hlzTStar"] == 4.2063
    assert compute_hlz_t_hurdle(103) == 4.2041

    base = {
        "strategy_id": "ADR0017_BOUNDARY_PROBE",
        "calibration_max_date": "2026-10-15",
        "cumulative_trials_n": 104,
        "clustered_t_stat": 4.50,
        "dsr_probability": 0.98,
        "cpcv_pbo": 0.10,
        "net_2x_cost_bps": 5.0,
        "max_protective_stop_pct": 1.5,
        "paper_closed_trades": 30,
        "alpaca_orders_per_min_cap": 200,
    }
    assert validate_promotion_candidate(PromotionCandidate(**base)) == (True, [])

    ok_dsr, dsr_reasons = validate_promotion_candidate(
        PromotionCandidate(**{**base, "dsr_probability": 0.95})
    )
    assert ok_dsr is False and len(dsr_reasons) == 1 and dsr_reasons[0].startswith("DSR_GATE_FAILED")

    ok_pbo, pbo_reasons = validate_promotion_candidate(PromotionCandidate(**{**base, "cpcv_pbo": 0.25}))
    assert ok_pbo is False and len(pbo_reasons) == 1 and pbo_reasons[0].startswith("CPCV_PBO_FAILED")

    ok_t, t_reasons = validate_promotion_candidate(PromotionCandidate(**{**base, "clustered_t_stat": 4.2062}))
    assert ok_t is False and len(t_reasons) == 1 and t_reasons[0].startswith("HLZ_HURDLE_FAILED")
