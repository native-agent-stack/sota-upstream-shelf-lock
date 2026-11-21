from __future__ import annotations

import re

from shelf_lock.starred_and_beyond_matrix import (
    BEYOND_STARRED_FRONTIER_SOTA_ANCHORS,
    LICENSE_AND_ARCHIVE_QUARANTINE_WATCHLIST,
    build_sota_research_convergence_matrix_manifest,
)

PERMISSIVE_OR_APPROVED_LICENSES = frozenset({"MIT", "Apache-2.0", "BSD-3-Clause", "LGPL-3.0"})
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def test_adr0026_frontier_llm_native_anchors_have_verified_shas_licenses_and_order_policies() -> None:
    required_new = (
        "nautechsystems/nautilus_agents",
        "anthropics/financial-services",
        "waylonli/FINSABER",
        "microsoft/MarS",
        "peernagy/LOBS5",
        "AI4Finance-Foundation/FinRobot",
        "HKUDS/Vibe-Trading",
        "aliyun/qwen-dianjin",
        "The-FinAI/Fino1",
        "The-FinAI/FinBen",
        "PriorLabs/TabPFN",
        "amazon-science/chronos-forecasting",
        "SalesforceAIResearch/uni2ts",
        "online-ml/river",
        "scikit-learn-contrib/MAPIE",
        "py-why/dowhy",
        "massive-com/mcp_massive",
        "BrainDAO/mcp-polymarket",
        "FreedomIntelligence/TwinMarket",
    )
    for slug in required_new:
        assert slug in BEYOND_STARRED_FRONTIER_SOTA_ANCHORS, f"Missing frontier anchor: {slug}"
        meta = BEYOND_STARRED_FRONTIER_SOTA_ANCHORS[slug]
        assert HEX40_RE.fullmatch(meta["head_sha"]), f"Non-40-char SHA on {slug}"
        assert meta["spdx_license"] in PERMISSIVE_OR_APPROVED_LICENSES, (
            f"Bad license on {slug}: {meta['spdx_license']}"
        )
        assert meta["layer_target"].startswith("L")
        assert meta["order_path_policy"].strip()
        assert slug not in LICENSE_AND_ARCHIVE_QUARANTINE_WATCHLIST

    manifest = build_sota_research_convergence_matrix_manifest()
    assert manifest["beyond_starred_frontier_anchors_count"] >= len(required_new) + 5


def test_adr0026_unlicensed_gpl_and_archived_repos_are_quarantined() -> None:
    quarantined = LICENSE_AND_ARCHIVE_QUARANTINE_WATCHLIST
    for slug in (
        "QuantaAlpha/QuantaAlpha",
        "SUFE-AIFLM-Lab/Fin-R1",
        "FinStep-AI/Alpha-R1",
        "horizon-llm/AlphaQuanter",
        "hansbuehler/deephedging",
        "OpenBB-finance/agents-for-openbb",
        "Polymarket/agents",
        "jpmorganchase/abides-jpmc-public",
        "hummingbot/mcp",
    ):
        assert slug in quarantined, f"Expected quarantined repo missing: {slug}"
        assert slug not in BEYOND_STARRED_FRONTIER_SOTA_ANCHORS
        assert HEX40_RE.fullmatch(quarantined[slug]["head_sha"])
        assert quarantined[slug]["reason"].strip()
