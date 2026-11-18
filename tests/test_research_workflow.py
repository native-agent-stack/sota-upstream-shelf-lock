from __future__ import annotations

import hashlib

from shelf_lock import (
    CANONICAL_RESEARCH_FEEDS_V2,
    CANONICAL_STRATEGY_ARCHETYPES,
    SIBLING_REPO_AUTHORITY,
    L1Event,
    compute_min_trl_fwer,
    evaluate_preregistration_power_gate,
    simulate_risk_adverse_buy_queue,
    verify_research_convergence_envelope,
)


def test_power_gate_rejects_underpowered_43_day_slice_and_approves_600_day_lake() -> None:
    short = evaluate_preregistration_power_gate(
        cumulative_trials_n=84,
        distinct_dates=43,
        daily_sigma_bps=45.0,
    )
    assert short.approved_to_preregister is False
    assert short.min_annualized_sharpe_to_pass > 9.5
    assert len(short.rejection_reasons) == 2

    full_lake = evaluate_preregistration_power_gate(
        cumulative_trials_n=85,
        distinct_dates=600,
        daily_sigma_bps=45.0,
    )
    assert full_lake.approved_to_preregister is True
    assert 2.60 < full_lake.min_annualized_sharpe_to_pass < 2.80
    assert full_lake.rejection_reasons == ()


def test_min_trl_fwer_increases_with_positive_autocorrelation_and_trials() -> None:
    trl_iid = compute_min_trl_fwer(0.20, cumulative_trials_n=10, autocorrelation=0.0)
    trl_ar1 = compute_min_trl_fwer(0.20, cumulative_trials_n=10, autocorrelation=0.25)
    trl_many = compute_min_trl_fwer(0.20, cumulative_trials_n=85, autocorrelation=0.25)
    assert trl_iid < trl_ar1 < trl_many


def test_risk_adverse_queue_requires_depletion_or_trade_through() -> None:
    # Initial displayed bid depth is 500 shares; we want 100 shares at $10.00.
    partial = simulate_risk_adverse_buy_queue(
        limit_price=10.00,
        initial_bid_size=500.0,
        order_qty=100.0,
        events=[
            L1Event(ts_ns=1, kind="trade", price=10.00, size=300.0),
            L1Event(ts_ns=2, kind="trade", price=10.01, size=900.0),
        ],
    )
    assert partial.filled is False
    assert partial.remaining_front_queue == 200.0

    # Depth shrinks from 500 -> 120, then 250 shares trade at $10.00 -> queue depleted (120 - 250 <= -100)
    depleted = simulate_risk_adverse_buy_queue(
        limit_price=10.00,
        initial_bid_size=500.0,
        order_qty=100.0,
        events=[
            L1Event(ts_ns=1, kind="quote", price=10.00, size=120.0),
            L1Event(ts_ns=2, kind="trade", price=10.00, size=250.0),
        ],
    )
    assert depleted.filled is True
    assert depleted.fill_reason == "queue_depleted"
    assert depleted.fill_price == 10.00

    # Strict trade-through at $9.99 fills immediately at $10.00
    through = simulate_risk_adverse_buy_queue(
        limit_price=10.00,
        initial_bid_size=5000.0,
        order_qty=100.0,
        events=[L1Event(ts_ns=5, kind="trade", price=9.99, size=50.0)],
    )
    assert through.filled is True
    assert through.fill_reason == "trade_through"
    assert through.fill_price == 10.00


def test_research_convergence_envelope_unites_18_pins_7_feeds_mintrl_queue_and_stop() -> None:
    assert len(CANONICAL_RESEARCH_FEEDS_V2) == 7
    assert CANONICAL_RESEARCH_FEEDS_V2["alpaca_boats"]["cutover_date"] == "2026-12-06"
    assert len(CANONICAL_STRATEGY_ARCHETYPES) == 4
    assert SIBLING_REPO_AUTHORITY == "PHILOSOPHY_ONLY"

    digest = hashlib.sha256(b"canonical-prewall-study-v2").hexdigest()
    ok_env = verify_research_convergence_envelope(
        input_sha256=digest,
        archetype="PRE_TRAVEL_EARLY_IGNITION",
        feeds_used=(
            "alpaca_sip",
            "alpaca_boats",
            "sec_edgar_acceptance_datetime",
            "finra_regsho_cnmsshvol_t1",
        ),
        study_max_date="2026-10-15",
        hard_stop_pct=1.75,
        cumulative_trials_n=85,
        distinct_dates=600,
        daily_sigma_bps=45.0,
        risk_adverse_queue_verified=True,
    )
    assert ok_env.approved is True
    assert ok_env.pinned_upstreams_verified == 18
    assert ok_env.violations == ()

    bad_env = verify_research_convergence_envelope(
        input_sha256="bad",
        archetype="UNKNOWN",
        feeds_used=("unsanctioned_feed",),
        study_max_date="2026-10-16",
        hard_stop_pct=2.50,
        cumulative_trials_n=85,
        distinct_dates=40,
        daily_sigma_bps=45.0,
        risk_adverse_queue_verified=False,
        sibling_repo_authority="DIRECT_IMPORT",
        upstream_pins={"alpaca-py": "bad_sha"},
    )
    assert bad_env.approved is False
    assert len(bad_env.violations) >= 8


def test_adr0010_two_stage_lit_to_collar_shelf_gate() -> None:
    from shelf_lock import evaluate_two_stage_lit_to_collar_shelf_gate

    ok = evaluate_two_stage_lit_to_collar_shelf_gate(
        initial_ask_px=100.00,
        ask_15s_px=100.07,
        bid_15s_px=100.00,
        ask_15s_lots=3.0,
        order_qty_shares=250.0,
    )
    assert ok["eligible_for_collar_fill"] is True
    assert ok["collar_fill_px"] == 100.07

    chased = evaluate_two_stage_lit_to_collar_shelf_gate(
        initial_ask_px=100.00,
        ask_15s_px=100.18,
        bid_15s_px=100.12,
        ask_15s_lots=5.0,
        order_qty_shares=250.0,
    )
    assert chased["eligible_for_collar_fill"] is False
    assert chased["collar_fill_px"] is None


def test_adr0011_h096_dry_powder_15s_bid_survival_and_informed_flow_joint_gate() -> None:
    from shelf_lock import evaluate_dry_powder_15s_bid_survival_collar_gate

    ok = evaluate_dry_powder_15s_bid_survival_collar_gate(
        initial_bid_px=99.94,
        initial_ask_px=100.00,
        min_lit_roundlot_px_0_15s=99.95,
        bid_15s_px=99.98,
        ask_15s_px=100.05,
        ask_15s_lots=4.0,
        order_qty_shares=250.0,
        ofi_entry=0.32,
        iso_f_buy_share=0.18,
    )
    assert ok["approved_dry_powder_collar"] is True
    assert ok["collar_fill_px"] == 100.05

    swept = evaluate_dry_powder_15s_bid_survival_collar_gate(
        initial_bid_px=99.94,
        initial_ask_px=100.00,
        min_lit_roundlot_px_0_15s=99.88,
        bid_15s_px=99.95,
        ask_15s_px=100.02,
        ask_15s_lots=4.0,
        order_qty_shares=250.0,
        ofi_entry=0.35,
        bjzz_inst_dark_share=0.16,
    )
    assert swept["approved_dry_powder_collar"] is False
    assert swept["bid_survived_15s"] is False

    weak_ofi = evaluate_dry_powder_15s_bid_survival_collar_gate(
        initial_bid_px=99.94,
        initial_ask_px=100.00,
        min_lit_roundlot_px_0_15s=None,
        bid_15s_px=99.96,
        ask_15s_px=100.04,
        ask_15s_lots=4.0,
        order_qty_shares=250.0,
        ofi_entry=0.08,
        iso_f_buy_share=0.0,
    )
    assert weak_ofi["approved_dry_powder_collar"] is False
    assert weak_ofi["informed_flow_ok"] is False


def test_adr0012_abnormal_rvol_tod_purges_megacap_normal_rate_size_bias() -> None:
    from shelf_lock import evaluate_abnormal_rvol_tod_shelf_gate

    megacap_normal = evaluate_abnormal_rvol_tod_shelf_gate(
        observed_cum_vol=10_100_000.0,
        expected_20d_tod_vol=10_000_000.0,
        ofi_entry=0.35,
    )
    assert megacap_normal["stage1_rvol_tod"] == 1.01
    assert megacap_normal["megacap_normal_rate_size_bias_purged"] is True
    assert megacap_normal["first_sign_admitted"] is False
    assert megacap_normal["early_ignition_admitted"] is False

    true_shock = evaluate_abnormal_rvol_tod_shelf_gate(
        observed_cum_vol=2_640_000.0,
        expected_20d_tod_vol=1_000_000.0,
        ofi_entry=0.32,
    )
    assert true_shock["stage1_rvol_tod"] == 2.64
    assert true_shock["megacap_normal_rate_size_bias_purged"] is False
    assert true_shock["first_sign_admitted"] is True
    assert true_shock["early_ignition_admitted"] is True


def test_adr0013_starred_413_and_beyond_sota_matrix_and_bitemporal_pit() -> None:
    from shelf_lock import (
        BEYOND_STARRED_FRONTIER_SOTA_ANCHORS,
        CONVERGENCE_MATRIX_SCHEMA_VERSION,
        FINALIZED_12_RANKING_FEED_IDS,
        STARRED_413_RESEARCH_ANCHORS,
        build_sota_research_convergence_matrix_manifest,
        verify_bitemporal_pit_event,
    )

    assert CONVERGENCE_MATRIX_SCHEMA_VERSION == "sota-research-convergence-matrix.v3.10"
    assert len(FINALIZED_12_RANKING_FEED_IDS) == 12
    assert "microsoft/qlib" in STARRED_413_RESEARCH_ANCHORS
    assert "microsoft/RD-Agent" in BEYOND_STARRED_FRONTIER_SOTA_ANCHORS
    assert "databento/databento-python" in BEYOND_STARRED_FRONTIER_SOTA_ANCHORS

    manifest = build_sota_research_convergence_matrix_manifest()
    assert manifest["immutable_core_pins_count"] == 18
    assert manifest["finalized_symbol_ranking_feeds_count"] == 12
    assert manifest["sibling_repo_authority"] == "PHILOSOPHY_ONLY"
    assert all(meta["authority"] == "PHILOSOPHY_ONLY" for meta in manifest["starred_413_anchors"].values())

    ok_pit, reasons_ok = verify_bitemporal_pit_event(1000, 1050, 1100)
    assert ok_pit is True and reasons_ok == []

    bad_recv, reasons_recv = verify_bitemporal_pit_event(1200, 1100, 1300)
    assert bad_recv is False and any("BITEMPORAL_CLOCK_SKEW_LOOKAHEAD" in r for r in reasons_recv)

    bad_dec, reasons_dec = verify_bitemporal_pit_event(1000, 1400, 1300)
    assert bad_dec is False and any("BITEMPORAL_DECISION_LOOKAHEAD" in r for r in reasons_dec)
