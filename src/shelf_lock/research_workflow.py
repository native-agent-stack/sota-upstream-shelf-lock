"""SOTA Pre-Registration Power (`MinTRL`/`MDE`) & `hftbacktest` Conservative Queue-Fill Research Gate.

Primary Upstream Citations (Pinned Shelf):
- `ml4t-diagnostic` (`19e76072e64a18c9ba56130e4a7bcc0bc871f57e`),
  `src/ml4t/diagnostic/evaluation/stats/minimum_track_record.py:160-191` (López de Prado, Lipton &
  Zoonekynd 2025, ADIA Lab Paper #19 Eq. 11 finite-sample autocorrelation/skew/kurtosis `MinTRL`).
- `hftbacktest` (`5f3ec40b2afb764e0fea112f941ed85523ef4e88`),
  `hftbacktest/src/backtest/models/queue.rs:63-96` (`RiskAdverseQueueModel`: queue initializes behind
  displayed L1 depth, decrements on same-price trades, clamps on depth shrinkage, fills on `front_q_qty < 0`
  or strict trade-through).
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from statistics import NormalDist

from shelf_lock.validator import HLZ_BASE_ALPHA, compute_hlz_t_hurdle


@dataclass(frozen=True)
class PreRegistrationPowerReport:
    cumulative_trials_n: int
    distinct_dates: int
    hlz_t_hurdle: float
    min_annualized_sharpe_to_pass: float
    mde_daily_bps_at_80pct_power: float
    min_trl_days_at_target_sr: float
    approved_to_preregister: bool
    rejection_reasons: tuple[str, ...]


@dataclass(frozen=True)
class L1Event:
    """Chronological post-signal L1 quote or trade event (`kind='trade'` or `kind='quote'`)."""

    ts_ns: int
    kind: str
    price: float
    size: float


@dataclass(frozen=True)
class PassiveQueueFillOutcome:
    filled: bool
    fill_price: float | None
    fill_ts_ns: int | None
    fill_reason: str
    remaining_front_queue: float


def compute_min_trl_fwer(
    observed_daily_sharpe: float,
    *,
    cumulative_trials_n: int = 1,
    target_daily_sharpe: float = 0.0,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
    autocorrelation: float = 0.0,
) -> float:
    """Exact finite-sample `MinTRL` under HLZ family-wise error rate (`ADIA Lab #19 Eq. 11`)."""
    sr_diff = observed_daily_sharpe - target_daily_sharpe
    if sr_diff <= 1e-10:
        return float("inf")

    z_alpha = (
        NormalDist().inv_cdf(0.95) if cumulative_trials_n <= 1 else compute_hlz_t_hurdle(cumulative_trials_n)
    )
    rho = autocorrelation
    if rho != 0.0 and abs(rho) < 1.0:
        coef_b = rho / (1.0 - rho)
        coef_c = (rho * rho) / (1.0 - rho * rho)
    else:
        coef_b = 0.0
        coef_c = 0.0

    a = 1.0 + 2.0 * coef_b
    b = 1.0 + coef_b + coef_c
    c = 1.0 + 2.0 * coef_c
    var_term = a - b * skewness * target_daily_sharpe + c * (kurtosis - 1.0) / 4.0 * (target_daily_sharpe**2)
    if var_term <= 0.0:
        return float("inf")
    min_trl = 1.0 + var_term * ((z_alpha / sr_diff) ** 2)
    return float(math.ceil(max(min_trl, 1.0)))


def evaluate_preregistration_power_gate(
    *,
    cumulative_trials_n: int,
    distinct_dates: int,
    daily_sigma_bps: float,
    plausible_annualized_sharpe: float = 3.0,
    max_feasible_annualized_sharpe: float = 5.0,
    power: float = 0.80,
    autocorrelation: float = 0.0,
) -> PreRegistrationPowerReport:
    """Block underpowered pre-registrations before burning trial multiplicity `N -> N + 1`."""
    if distinct_dates < 1 or daily_sigma_bps <= 0.0:
        raise ValueError("distinct_dates >= 1 and daily_sigma_bps > 0 required")

    t_star = compute_hlz_t_hurdle(cumulative_trials_n)
    years = distinct_dates / 252.0
    sr_min_ann = t_star / math.sqrt(years)
    z_power = NormalDist().inv_cdf(power)
    mde_bps = (t_star + z_power) * (daily_sigma_bps / math.sqrt(distinct_dates))
    plausible_daily_sr = plausible_annualized_sharpe / math.sqrt(252.0)
    min_trl_days = compute_min_trl_fwer(
        plausible_daily_sr,
        cumulative_trials_n=cumulative_trials_n,
        autocorrelation=autocorrelation,
    )

    reasons: list[str] = []
    if distinct_dates < 60:
        reasons.append(f"Insufficient distinct trading dates ({distinct_dates} < 60 minimum)")
    if sr_min_ann > max_feasible_annualized_sharpe:
        reasons.append(
            f"Underpowered sample: clearing HLZ t*={t_star:.4f} over {distinct_dates} dates requires "
            f"annualized SR >= {sr_min_ann:.2f} (> {max_feasible_annualized_sharpe:.2f} ceiling)"
        )

    return PreRegistrationPowerReport(
        cumulative_trials_n=cumulative_trials_n,
        distinct_dates=distinct_dates,
        hlz_t_hurdle=round(t_star, 4),
        min_annualized_sharpe_to_pass=round(sr_min_ann, 4),
        mde_daily_bps_at_80pct_power=round(mde_bps, 4),
        min_trl_days_at_target_sr=min_trl_days,
        approved_to_preregister=(len(reasons) == 0),
        rejection_reasons=tuple(reasons),
    )


def simulate_risk_adverse_buy_queue(
    *,
    limit_price: float,
    initial_bid_size: float,
    order_qty: float,
    events: Sequence[L1Event],
    tick_eps: float = 1e-6,
) -> PassiveQueueFillOutcome:
    """Simulate conservative passive buy limit execution per `hftbacktest::RiskAdverseQueueModel`."""
    if limit_price <= 0.0 or order_qty <= 0.0 or initial_bid_size < 0.0:
        raise ValueError("Invalid limit_price, order_qty, or initial_bid_size")

    front_q_qty = float(initial_bid_size)
    for ev in events:
        if ev.kind == "trade":
            if ev.price < limit_price - tick_eps:
                return PassiveQueueFillOutcome(
                    filled=True,
                    fill_price=limit_price,
                    fill_ts_ns=ev.ts_ns,
                    fill_reason="trade_through",
                    remaining_front_queue=0.0,
                )
            if abs(ev.price - limit_price) <= tick_eps:
                front_q_qty -= ev.size
                if front_q_qty + tick_eps <= -order_qty:
                    return PassiveQueueFillOutcome(
                        filled=True,
                        fill_price=limit_price,
                        fill_ts_ns=ev.ts_ns,
                        fill_reason="queue_depleted",
                        remaining_front_queue=0.0,
                    )
        elif ev.kind == "quote":
            if ev.price < limit_price - tick_eps:
                return PassiveQueueFillOutcome(
                    filled=True,
                    fill_price=limit_price,
                    fill_ts_ns=ev.ts_ns,
                    fill_reason="ask_or_bid_crossed",
                    remaining_front_queue=0.0,
                )
            if abs(ev.price - limit_price) <= tick_eps:
                front_q_qty = min(front_q_qty, max(0.0, ev.size))

    return PassiveQueueFillOutcome(
        filled=False,
        fill_price=None,
        fill_ts_ns=None,
        fill_reason="expired_unfilled",
        remaining_front_queue=round(max(0.0, front_q_qty), 4),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="SOTA Pre-Registration Power & Queue-Fill Gate")
    parser.add_argument("--trials-n", type=int, default=85)
    parser.add_argument("--dates", type=int, default=600)
    parser.add_argument("--sigma-bps", type=float, default=45.0)
    args = parser.parse_args()

    rep = evaluate_preregistration_power_gate(
        cumulative_trials_n=args.trials_n,
        distinct_dates=args.dates,
        daily_sigma_bps=args.sigma_bps,
    )
    print(
        json.dumps(
            {
                "approved": rep.approved_to_preregister,
                "hlz_base_alpha": HLZ_BASE_ALPHA,
                "hlz_t_hurdle": rep.hlz_t_hurdle,
                "min_annualized_sharpe_to_pass": rep.min_annualized_sharpe_to_pass,
                "mde_daily_bps_at_80pct_power": rep.mde_daily_bps_at_80pct_power,
                "min_trl_days_at_sr3": rep.min_trl_days_at_target_sr,
                "rejection_reasons": list(rep.rejection_reasons),
            },
            indent=2,
        )
    )
    return 0 if rep.approved_to_preregister else 1


if __name__ == "__main__":
    raise SystemExit(main())
