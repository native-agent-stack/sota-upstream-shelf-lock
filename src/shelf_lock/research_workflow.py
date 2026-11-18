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
import datetime as dt
import json
import math
import pathlib
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import NormalDist

from shelf_lock.validator import HEX40_RE, HLZ_BASE_ALPHA, compute_hlz_t_hurdle, load_pins_lock

RESEARCH_FEEDS_SCHEMA_VERSION = "sota-research-feeds.v2"
SIBLING_REPO_AUTHORITY = "PHILOSOPHY_ONLY"
STUDY_WALL_ISO = "2026-10-15"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

CANONICAL_STRATEGY_ARCHETYPES: tuple[str, ...] = (
    "PRE_TRAVEL_EARLY_IGNITION",
    "FIRST_HAND_SEC_EPISODIC_PIVOT",
    "MEGA_CAP_NEAR_LOSSLESS_ORB",
    "CLIMAX_VWAP_MEAN_REVERSION",
)

CANONICAL_RESEARCH_FEEDS_V2: dict[str, dict[str, object]] = {
    "alpaca_sip": {
        "window_et": "04:00-20:00 ET Mon-Fri",
        "upstream": "alpaca-py",
        "pit_rule": "Nanosecond UTC trade/NBBO alignment; HostPinnedPacedAdapter <=185 req/min; ISO 'F' != odd-lot 'I'",
    },
    "alpaca_boats": {
        "window_et": "20:00-04:00 ET Sun-Fri",
        "cutover_date": "2026-12-06",
        "cutover_mode": "23/5 SIP cutover gated by SOTA_ENABLE_DEC6_235_SIP (default 0)",
        "upstream": "alpaca-py",
        "pit_rule": "900s stale-print expiry; timestamp guard so BOATS never overwrites newer Premarket SIP",
    },
    "alpaca_raw_vs_all_adjustment": {
        "window_et": "Intraday execution (RAW) vs multi-day historical series (ALL)",
        "upstream": "alpaca-py",
        "pit_rule": "Adjustment.RAW for unadjusted fill/NBBO parity; Adjustment.ALL for multi-day return series",
    },
    "sec_edgar_acceptance_datetime": {
        "window_et": "06:00-22:00 ET Mon-Fri SEC EDGAR Atom & submissions",
        "half_life_minutes": 15,
        "dilution_block_forms": ("424B2", "424B3", "424B4", "424B5", "S-3", "S-3ASR", "F-3"),
        "upstream": "edgartools",
        "pit_rule": "acceptanceDateTime <= as_of_utc with 15m freshness half-life + instant 424B*/S-3 dilution block",
    },
    "finra_regsho_cnmsshvol_t1": {
        "window_et": "Post-EOD T-1 trading-day lag",
        "lag_trading_days": 1,
        "upstream": "duckdb",
        "pit_rule": "Strict CNMSshvol d_tag < target_tag (T-1 lag); zero same-day short-volume lookahead",
    },
    "corporate_actions_split_guard": {
        "window_et": "XNYS pre-open corporate-actions & holiday calendar",
        "upstream": "exchange_calendars",
        "pit_rule": "Ex-date split/reverse-split discontinuity quarantine + XNYS holiday/early-close entry pause",
    },
    "ibkr_paper_4002_l1": {
        "window_et": "24/5 outsideRth L1 quote & protective stop lane (:4002 Paper only)",
        "paper_port": 4002,
        "forbidden_live_ports": (4001, 7496),
        "upstream": "ib_async",
        "pit_rule": "Paper-only gateway on 127.0.0.1:4002 (<=3,000 msg/min); live ports 4001/7496 hard-refused",
    },
}


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


@dataclass(frozen=True)
class ResearchConvergenceEnvelopeReport:
    approved: bool
    schema_version: str
    sibling_repo_authority: str
    pinned_upstreams_verified: int
    power_report: PreRegistrationPowerReport
    violations: tuple[str, ...]


def verify_research_convergence_envelope(
    *,
    input_sha256: str,
    archetype: str,
    feeds_used: Sequence[str],
    study_max_date: str,
    hard_stop_pct: float,
    cumulative_trials_n: int,
    distinct_dates: int,
    daily_sigma_bps: float,
    risk_adverse_queue_verified: bool = True,
    sibling_repo_authority: str = SIBLING_REPO_AUTHORITY,
    upstream_pins: Mapping[str, str] | None = None,
    repo_root: pathlib.Path | None = None,
) -> ResearchConvergenceEnvelopeReport:
    """Unite 18-repo 40-hex upstream pins, 64-hex input SHA-256, 7-feed PIT, MinTRL/MDE, QueueModel & ADR-0022."""
    violations: list[str] = []

    if not isinstance(input_sha256, str) or not HEX64_RE.fullmatch(input_sha256):
        violations.append("ADR0004_INVALID_INPUT_SHA256: expected 64-char lowercase hex digest")

    if archetype not in CANONICAL_STRATEGY_ARCHETYPES:
        violations.append(f"UNKNOWN_STRATEGY_ARCHETYPE: {archetype!r}")

    if not feeds_used:
        violations.append("EMPTY_DATAFEEDS: at least one canonical sota-research-feeds.v2 feed required")
    else:
        unknown_feeds = [f for f in feeds_used if f not in CANONICAL_RESEARCH_FEEDS_V2]
        if unknown_feeds:
            violations.append(f"UNSANCTIONED_DATAFEEDS: {unknown_feeds}")

    try:
        parsed_date = dt.date.fromisoformat(study_max_date)
        if parsed_date > dt.date.fromisoformat(STUDY_WALL_ISO):
            violations.append(f"PREWALL_VIOLATION: {study_max_date} > {STUDY_WALL_ISO}")
    except (TypeError, ValueError):
        violations.append(f"INVALID_STUDY_MAX_DATE: {study_max_date!r}")

    if (
        isinstance(hard_stop_pct, bool)
        or not isinstance(hard_stop_pct, (int, float))
        or not math.isfinite(float(hard_stop_pct))
        or not (0.0 < float(hard_stop_pct) <= 2.0)
    ):
        violations.append(f"ADR0022_STOP_VIOLATION: hard_stop_pct={hard_stop_pct} outside (0.0, 2.00]")

    if not risk_adverse_queue_verified:
        violations.append("QUEUE_MODEL_UNVERIFIED: hftbacktest RiskAdverseQueueModel check required")

    if sibling_repo_authority != SIBLING_REPO_AUTHORITY:
        violations.append(
            f"SIBLING_AUTHORITY_VIOLATION: expected {SIBLING_REPO_AUTHORITY!r}, got {sibling_repo_authority!r}"
        )

    lock_doc = load_pins_lock(repo_root)
    canonical_pin_map = {str(p["name"]): str(p["commit"]) for p in lock_doc.get("upstreamShelfPins", [])}
    pins_to_check = dict(upstream_pins) if upstream_pins is not None else canonical_pin_map
    verified_pins = 0
    if len(pins_to_check) != 18:
        violations.append(f"UPSTREAM_PIN_COUNT_MISMATCH: expected 18 pins, got {len(pins_to_check)}")
    for name, sha in sorted(pins_to_check.items()):
        if not HEX40_RE.fullmatch(str(sha)) or canonical_pin_map.get(name) != str(sha):
            violations.append(f"UPSTREAM_SHA_DRIFT: {name}={sha}")
        else:
            verified_pins += 1

    power_rep = evaluate_preregistration_power_gate(
        cumulative_trials_n=cumulative_trials_n,
        distinct_dates=max(1, distinct_dates),
        daily_sigma_bps=max(1e-6, daily_sigma_bps),
    )
    if not power_rep.approved_to_preregister:
        violations.extend(f"POWER_GATE_REJECTED: {r}" for r in power_rep.rejection_reasons)

    return ResearchConvergenceEnvelopeReport(
        approved=(len(violations) == 0),
        schema_version=RESEARCH_FEEDS_SCHEMA_VERSION,
        sibling_repo_authority=sibling_repo_authority,
        pinned_upstreams_verified=verified_pins,
        power_report=power_rep,
        violations=tuple(violations),
    )


def evaluate_two_stage_lit_to_collar_shelf_gate(
    *,
    initial_ask_px: float,
    ask_15s_px: float,
    bid_15s_px: float,
    ask_15s_lots: float,
    order_qty_shares: float,
    max_collar_bps: float = 10.0,
) -> dict[str, object]:
    """Validate Stage-2 `15s` lit-bid -> `<= 10.0 bps` collar escalation (`ADR-0010` / `H095`)."""
    vals = (initial_ask_px, ask_15s_px, bid_15s_px, ask_15s_lots, order_qty_shares, max_collar_bps)
    if any(
        isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(float(v)) for v in vals
    ):
        raise ValueError("All Stage-2 collar gate inputs must be finite real numbers")
    if initial_ask_px <= 0.0 or bid_15s_px <= 0.0 or ask_15s_px < bid_15s_px or order_qty_shares <= 0.0:
        raise ValueError("Invalid prices or order_qty_shares for Stage-2 collar gate")
    if not (0.0 < max_collar_bps <= 10.0):
        raise ValueError("max_collar_bps must lie in (0.0, 10.0]")

    mid_15s = 0.5 * (bid_15s_px + ask_15s_px)
    spread_15s_bps = ((ask_15s_px - bid_15s_px) / mid_15s) * 10_000.0
    collar_ceiling_px = initial_ask_px * (1.0 + max_collar_bps / 10_000.0)
    displayed_shares = ask_15s_lots * 100.0
    eligible = (
        ask_15s_px <= collar_ceiling_px + 1e-9
        and 0.0 < spread_15s_bps <= max_collar_bps
        and displayed_shares >= order_qty_shares
    )
    return {
        "eligible_for_collar_fill": eligible,
        "collar_fill_px": round(ask_15s_px, 4) if eligible else None,
        "collar_ceiling_px": round(collar_ceiling_px, 4),
        "spread_15s_bps": round(spread_15s_bps, 4),
        "displayed_ask_shares": round(displayed_shares, 2),
    }


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
