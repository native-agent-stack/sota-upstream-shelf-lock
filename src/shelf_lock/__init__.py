"""Immutable 40-char upstream SHA lock & 5-stage Sim->Alpaca/IBKR promotion validator."""

from .validator import (
    HLZ_BASE_ALPHA,
    PromotionCandidate,
    compute_hlz_t_hurdle,
    load_pins_lock,
    scan_repo_privacy_hygiene,
    validate_pins_lock,
    validate_promotion_candidate,
)

__all__ = [
    "HLZ_BASE_ALPHA",
    "PromotionCandidate",
    "compute_hlz_t_hurdle",
    "load_pins_lock",
    "scan_repo_privacy_hygiene",
    "validate_pins_lock",
    "validate_promotion_candidate",
]
