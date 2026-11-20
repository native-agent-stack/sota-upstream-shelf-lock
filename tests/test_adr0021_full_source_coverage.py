"""Tests for ADR-0021 Full 4-Tier SOTA Source Coverage, Validator Expansion & Low-Quality Purge."""

from __future__ import annotations

import json
import re
from pathlib import Path

from shelf_lock.validator import ALLOWED_LICENSES, compute_hlz_t_hurdle, load_pins_lock

REPO_ROOT = Path(__file__).resolve().parents[1]
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def test_adr0021_validator_allows_osi_permissive_ncsa_and_bsd2_only() -> None:
    assert {
        "MIT",
        "Apache-2.0",
        "BSD-3-Clause",
        "BSD-2-Clause",
        "NCSA",
        "LGPL-3.0-or-later",
    } == ALLOWED_LICENSES
    for blocked in ("GPL-3.0", "AGPL-3.0", "AGPL-3.0-only", "BUSL-1.1", "Commons-Clause-1.0", "Proprietary"):
        assert blocked not in ALLOWED_LICENSES


def test_adr0021_full_4tier_source_coverage_and_low_quality_purge() -> None:
    catalog = json.loads((REPO_ROOT / "STARRED_CONVERGENCE_CATALOG.json").read_text(encoding="utf-8"))
    pins_doc = load_pins_lock(REPO_ROOT)

    blk = catalog["fullSourceCoverageAndStarredManifest"]
    assert blk["schemaId"] == "sota-v3114-full-source-coverage-and-cleanup.v1"
    assert blk["adr"] == "ADR-0021"
    assert blk["immutableCorePinsUntouched"] == len(pins_doc["upstreamShelfPins"]) == 18
    assert blk["orderAuthority"] is False
    assert blk["standaloneAlphaClaim"] is False
    assert blk["hlzTrialConsumed"] is False
    assert blk["nextTrialId"] == 105
    assert blk["nextHlzTStar"] == compute_hlz_t_hurdle(105) == 4.2084
    assert set(blk["validatorAllowedLicensesExpanded"]) == ALLOWED_LICENSES

    receipt = blk["githubStarSyncReceipt"]
    assert receipt["newlyStarredElitePermissiveCount"] == 50
    assert receipt["failedStarCount"] == 0
    assert receipt["core18AllStarred"] is True
    assert receipt["frontier18AllStarred"] is True
    assert receipt["officialCommunityBeyond19AllStarred"] is True

    # ADR-0018 refreshed pointers
    refreshed = blk["adr0018RefreshedPointers"]
    assert refreshed["qlib"]["ref"] == "v0.9.8"
    assert HEX40_RE.fullmatch(refreshed["qlib"]["commit"])
    assert refreshed["openbbWorkspaceBackendSdk"]["repo"] == "openbq-org/backends-for-openbb"
    assert refreshed["openbbPlatformV5"]["license"] == "Apache-2.0"

    # Official regulatory & exchange sources
    assert len(blk["officialRegulatoryAndExchangePrimarySources"]) == 7

    # 19 official/foundation/institutional/community/beyond repos all SHA-verified & OSI-permissive
    extra19 = blk["officialCommunityAndBeyondStarred19"]
    assert len(extra19) == 19
    for row in extra19:
        assert HEX40_RE.fullmatch(row["commit"]), row["repo"]
        assert row["license"] in ALLOWED_LICENSES, row["repo"]
        assert row["orderAuthority"] is False

    # Every ADR-0020 frontier lib is now cleanly inside ALLOWED_LICENSES too
    for row in catalog["advancedStrategyAndSimMeritLandscape"]["permissiveFrontierLibraries"]:
        assert row["license"] in ALLOWED_LICENSES, row["repo"]

    # Low-quality & banned sources denylist
    purged = {row["source"] for row in blk["lowQualityAndBannedSourcesPurged"]}
    assert {
        "ranaroussi/yfinance",
        "mementum/backtrader",
        "kernc/backtesting.py",
        "cvxgrp/cvxportfolio",
        "man-group/ArcticDB",
        "hudson-and-thames/mlfinlab",
        "google-research/timesfm (v3.0 weights)",
    } <= purged
