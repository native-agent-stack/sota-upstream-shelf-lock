from __future__ import annotations

from shelf_lock import (
    L1Event,
    compute_min_trl_fwer,
    evaluate_preregistration_power_gate,
    simulate_risk_adverse_buy_queue,
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
