from __future__ import annotations

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
