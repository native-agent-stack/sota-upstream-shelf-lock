"""Tests for ADR-0020 Advanced Strategy Sources, Frontier OSS Libraries & License Firewall."""

from __future__ import annotations

import json
import re
from pathlib import Path

from shelf_lock.validator import ALLOWED_LICENSES, compute_hlz_t_hurdle, load_pins_lock

REPO_ROOT = Path(__file__).resolve().parents[1]
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def test_adr0020_advanced_strategy_sim_merit_landscape_contract() -> None:
    catalog = json.loads((REPO_ROOT / "STARRED_CONVERGENCE_CATALOG.json").read_text(encoding="utf-8"))
    pins_doc = load_pins_lock(REPO_ROOT)

    block = catalog["advancedStrategyAndSimMeritLandscape"]
    assert block["schemaId"] == "sota-v3113-advanced-strategy-sim-merit-landscape.v1"
    assert block["adr"] == "ADR-0020"
    assert block["immutableCorePinsUntouched"] == len(pins_doc["upstreamShelfPins"]) == 18
    assert block["orderAuthority"] is False
    assert block["standaloneAlphaClaim"] is False
    assert block["promotionTrack"] == "PROTECTIVE_FILTER_OR_GOVERNANCE"
    assert block["hlzTrialConsumed"] is False
    assert block["nextTrialId"] == 105
    assert block["nextHlzTStar"] == compute_hlz_t_hurdle(105) == 4.2084
    assert block["livePortsRefused"] == [4001, 7496, 8796, 8798]
    assert block["liveHostsRefused"] == ["api.alpaca.markets"]

    # Advisories for ADR-0018 refresh
    advisories = {a["name"]: a for a in block["adr0018SecurityAndLicenseAdvisories"]}
    assert {
        "qlib-v098-security-bump",
        "openbq-backends-for-openbb-successor",
        "openbq-openbb-v5-apache2-relicense",
    } <= set(advisories)
    for adv in advisories.values():
        assert HEX40_RE.fullmatch(adv["commit"])
        assert adv["license"] in ALLOWED_LICENSES

    # Permissive frontier libraries
    libs = block["permissiveFrontierLibraries"]
    assert len(libs) == 18
    ranks = [row["roiRank"] for row in libs]
    assert ranks == list(range(1, 19))
    for row in libs:
        assert HEX40_RE.fullmatch(row["commit"]), row["repo"]
        assert row["osiPermissive"] is True
        assert row["orderAuthority"] is False
        assert row["class"] == "OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH"
        if not row["requiresValidatorLicenseAdr"]:
            assert row["license"] in ALLOWED_LICENSES, row["repo"]
        else:
            assert row["license"] in {"NCSA", "BSD-2-Clause"}, row["repo"]

    # Non-permissive / archived license firewall
    blocked = {row["repo"]: row for row in block["licenseFirewallBlockedOrPhilosophyOnly"]}
    assert {
        "cvxgrp/cvxportfolio",
        "freqtrade/freqtrade",
        "kernc/backtesting.py",
        "edtechre/pybroker",
        "man-group/ArcticDB",
        "hudson-and-thames/mlfinlab",
        "jpmorganchase/abides-jpmc-public",
    } <= set(blocked)
    for row in blocked.values():
        assert row["class"] == "PHILOSOPHY_ONLY"
        if "commit" in row:
            assert HEX40_RE.fullmatch(row["commit"]), row["repo"]

    # 6 frontier academic families
    families = block["frontierAcademicStrategyFamilies"]
    assert len(families) == 6
    assert all(len(f["citations"]) >= 3 for f in families)
    assert all(
        all(
            u.startswith(
                ("https://doi.org/", "https://arxiv.org/", "https://papers.ssrn.com/", "https://ssrn.com/")
            )
            for u in f["citations"]
        )
        for f in families
    )
