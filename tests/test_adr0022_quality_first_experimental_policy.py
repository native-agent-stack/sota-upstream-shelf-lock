"""Tests for ADR-0022 Quality-First Experimental SOTA Policy & Wave-2 Star Expansion."""

from __future__ import annotations

import json
import re
from pathlib import Path

from shelf_lock.validator import (
    EXPERIMENTAL_ENV_EVALUATION_POLICY,
    EXPERIMENTAL_QUALITY_FIRST_ALLOW_ALL_LICENSES,
    compute_hlz_t_hurdle,
    evaluate_experimental_repo_eligibility,
    load_pins_lock,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def test_adr0022_experimental_evaluator_judges_strictly_on_technical_sota_quality() -> None:
    assert EXPERIMENTAL_ENV_EVALUATION_POLICY == "QUALITY_AND_SOTA_ONLY_NO_LICENSE_EXCLUSION"
    assert EXPERIMENTAL_QUALITY_FIRST_ALLOW_ALL_LICENSES is True

    # Technically SOTA repos pass regardless of GPL-3.0 / BUSL-1.1 / Non-Commercial / MPL-2.0
    for repo, lic in (
        ("cvxgrp/cvxportfolio", "GPL-3.0"),
        ("man-group/ArcticDB", "BUSL-1.1"),
        ("google-research/timesfm", "Non-Commercial-v3.0"),
        ("xtdb/xtdb", "MPL-2.0"),
    ):
        ok, reasons = evaluate_experimental_repo_eligibility(
            repo,
            actively_maintained=True,
            institutional_or_sota_caliber=True,
            uses_official_or_verifiable_data=True,
            single_asset_toy_only=False,
            license_id=lic,
        )
        assert ok is True and reasons == []

    # Technically low-quality / stale / scraper / single-asset toys STILL fail regardless of license!
    ok_yf, r_yf = evaluate_experimental_repo_eligibility(
        "ranaroussi/yfinance",
        actively_maintained=True,
        institutional_or_sota_caliber=False,
        uses_official_or_verifiable_data=False,
        license_id="Apache-2.0",
    )
    assert ok_yf is False
    assert "TECHNICAL_FAIL_FRAGILE_SCRAPER_OR_UNVERIFIABLE_DATA" in r_yf

    ok_bt, r_bt = evaluate_experimental_repo_eligibility(
        "kernc/backtesting.py",
        actively_maintained=True,
        institutional_or_sota_caliber=False,
        single_asset_toy_only=True,
        license_id="MIT",
    )
    assert ok_bt is False
    assert "TECHNICAL_FAIL_SINGLE_ASSET_TOY_SCOPE" in r_bt


def test_adr0022_catalog_wave2_star_receipt_and_unblocked_sota_shas() -> None:
    catalog = json.loads((REPO_ROOT / "STARRED_CONVERGENCE_CATALOG.json").read_text(encoding="utf-8"))
    pins_doc = load_pins_lock(REPO_ROOT)
    blk = catalog["experimentalQualityFirstSotaExpansion"]

    assert blk["schemaId"] == "sota-v3115-experimental-quality-first-sota.v1"
    assert blk["adr"] == "ADR-0022"
    assert blk["ownerDirectivePolicy"] == "QUALITY_AND_SOTA_ONLY_NO_LICENSE_EXCLUSION"
    assert blk["allowAllLicensesForExperimentalRd"] is True
    assert blk["immutableCorePinsUntouched"] == len(pins_doc["upstreamShelfPins"]) == 18
    assert blk["orderAuthority"] is False
    assert blk["hlzTrialConsumed"] is False
    assert blk["nextTrialId"] == 105
    assert blk["nextHlzTStar"] == compute_hlz_t_hurdle(105) == 4.2084

    rcpt = blk["wave2StarSyncReceipt"]
    assert rcpt["wave1NewlyStarredCount"] == 50
    assert rcpt["wave2NewlyStarredCount"] == 58
    assert rcpt["cumulativeNewSotaStarsToday"] == 108
    assert rcpt["failedStarCount"] == 0

    unblocked = {r["repo"]: r for r in blk["unblockedTechnicallySotaRepos"]}
    assert {
        "cvxgrp/cvxportfolio",
        "man-group/ArcticDB",
        "google-research/timesfm",
        "xtdb/xtdb",
        "edtechre/pybroker",
        "freqtrade/freqtrade",
    } == set(unblocked)
    for row in unblocked.values():
        assert HEX40_RE.fullmatch(row["commit"]), row["repo"]
        assert row["orderAuthority"] is False

    wave2 = blk["wave2FlagshipSotaAdditions19"]
    assert len(wave2) == 19
    for row in wave2:
        assert HEX40_RE.fullmatch(row["commit"]), row["repo"]
        assert row["orderAuthority"] is False

    tech_rejected = {r["source"] for r in blk["technicalQualityOnlyRejections"]}
    assert {
        "ranaroussi/yfinance",
        "mementum/backtrader",
        "kernc/backtesting.py",
        "hudson-and-thames/mlfinlab",
    } <= (tech_rejected)
