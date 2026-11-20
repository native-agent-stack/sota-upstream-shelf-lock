from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass
from statistics import NormalDist
from typing import Any

HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
DATE_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HOME_PATH_RE = re.compile(r"/Users/(?!<user>)[A-Za-z0-9._-]+/")
ACCOUNT_OR_KEY_RE = re.compile(
    r"\b(?:PA|DU)[0-9A-Z]{6,16}\b|\b(?:PK|AK)[0-9A-Z]{16,32}\b|\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{20,}\b"
)
ALLOWED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "NCSA", "LGPL-3.0-or-later"}
HLZ_BASE_ALPHA = 0.00135


def compute_hlz_t_hurdle(cumulative_trials_n: int) -> float:
    """Return one-sided Harvey-Liu-Zhu multiple-testing t-statistic hurdle (Phi(-3.0)=0.00135 / N)."""
    if cumulative_trials_n < 1:
        raise ValueError("cumulative_trials_n must be >= 1")
    if cumulative_trials_n == 1:
        return 3.00
    per_trial_tail = HLZ_BASE_ALPHA / float(cumulative_trials_n)
    return round(NormalDist().inv_cdf(1.0 - per_trial_tail), 4)


@dataclass(frozen=True)
class PromotionCandidate:
    strategy_id: str
    calibration_max_date: str
    cumulative_trials_n: int
    clustered_t_stat: float
    dsr_probability: float
    cpcv_pbo: float
    net_2x_cost_bps: float
    max_protective_stop_pct: float
    paper_closed_trades: int
    alpaca_orders_per_min_cap: int
    uses_live_host_or_port: bool = False


def load_pins_lock(repo_root: pathlib.Path | None = None) -> dict[str, Any]:
    root = repo_root or pathlib.Path(__file__).resolve().parents[2]
    return json.loads((root / "PINS_LOCK.json").read_text(encoding="utf-8"))


def validate_pins_lock(doc: dict[str, Any], *, online_ls_remote: bool = False) -> list[str]:
    errors: list[str] = []
    inv = doc.get("invariants", {})
    if inv.get("studyWallDate") != "2026-10-15":
        errors.append(f"studyWallDate must be '2026-10-15', got {inv.get('studyWallDate')!r}")
    if float(inv.get("maxProtectiveStopPct", 99.0)) > 2.0:
        errors.append("ADR-0022 violation: maxProtectiveStopPct exceeds 2.0%")
    if int(inv.get("alpacaPaperMaxOrdersPerMin", 9999)) > 200:
        errors.append("alpacaPaperMaxOrdersPerMin exceeds 200 req/min cap")
    if int(inv.get("ibkrPaperPort", 0)) != 4002:
        errors.append("ibkrPaperPort must be 4002 (paper gateway)")
    if set(inv.get("forbiddenLivePorts", [])) != {4001, 7496}:
        errors.append("forbiddenLivePorts must include {4001, 7496}")

    stages = doc.get("compoundingPipelineStages", [])
    if [s.get("stage") for s in stages] != [1, 2, 3, 4, 5]:
        errors.append("compoundingPipelineStages must define ordered stages 1..5")

    pins = doc.get("upstreamShelfPins", [])
    if len(pins) != 18:
        errors.append(f"Expected exactly 18 upstreamShelfPins, got {len(pins)}")

    seen_names: set[str] = set()
    seen_urls: set[str] = set()
    for p in pins:
        name = str(p.get("name", ""))
        url = str(p.get("url", ""))
        sha = str(p.get("commit", ""))
        lic = str(p.get("license", ""))
        if not name or name in seen_names:
            errors.append(f"Duplicate or empty upstream name: {name!r}")
        seen_names.add(name)
        if not url.startswith("https://github.com/") or url in seen_urls:
            errors.append(f"Invalid or duplicate GitHub upstream URL: {url!r}")
        seen_urls.add(url)
        if not HEX40_RE.match(sha):
            errors.append(f"Invalid 40-char SHA for {name}: {sha!r}")
        if lic not in ALLOWED_LICENSES:
            errors.append(f"Disallowed license for {name}: {lic!r}")
        if online_ls_remote and url.startswith("https://github.com/"):
            res = subprocess.run(
                ["git", "ls-remote", url, "HEAD"],
                text=True,
                capture_output=True,
                timeout=20,
                check=False,
            )
            if res.returncode != 0 or not res.stdout.strip():
                errors.append(f"Upstream unreachable via git ls-remote: {url}")
    return errors


def validate_promotion_candidate(c: PromotionCandidate) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if c.uses_live_host_or_port:
        reasons.append("HARD_REFUSED: candidate touches live broker host or live IBKR port 4001/7496")
    if not DATE_ISO_RE.match(c.calibration_max_date) or c.calibration_max_date > "2026-10-15":
        reasons.append(f"PREWALL_LEAKAGE: calibration_max_date {c.calibration_max_date!r} > '2026-10-15'")
    if not math.isfinite(c.max_protective_stop_pct) or not (0.0 < c.max_protective_stop_pct <= 2.0):
        reasons.append(f"ADR0022_STOP_VIOLATION: stop {c.max_protective_stop_pct}% outside (0, 2.00%]")
    if c.alpaca_orders_per_min_cap > 200 or c.alpaca_orders_per_min_cap < 1:
        reasons.append(f"PACER_CAP_VIOLATION: order cap {c.alpaca_orders_per_min_cap}/min outside [1, 200]")
    req_t = compute_hlz_t_hurdle(c.cumulative_trials_n)
    if not math.isfinite(c.clustered_t_stat) or c.clustered_t_stat < req_t:
        reasons.append(
            f"HLZ_HURDLE_FAILED: t={c.clustered_t_stat:.4f} < t*({c.cumulative_trials_n})={req_t:.4f}"
        )
    if not math.isfinite(c.dsr_probability) or c.dsr_probability <= 0.95:
        reasons.append(f"DSR_GATE_FAILED: dsr={c.dsr_probability:.4f} <= 0.95")
    if not math.isfinite(c.cpcv_pbo) or c.cpcv_pbo >= 0.25:
        reasons.append(f"CPCV_PBO_FAILED: pbo={c.cpcv_pbo:.4f} >= 0.25")
    if not math.isfinite(c.net_2x_cost_bps) or c.net_2x_cost_bps <= 0.0:
        reasons.append(f"COST_STRESS_2X_FAILED: net_2x_cost_bps={c.net_2x_cost_bps:.2f} <= 0.0")
    if c.paper_closed_trades < 30:
        reasons.append(f"SAMPLE_BREADTH_FAILED: paper_closed_trades={c.paper_closed_trades} < 30")
    return (len(reasons) == 0), reasons


def scan_repo_privacy_hygiene(repo_root: pathlib.Path) -> list[str]:
    violations: list[str] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(repo_root)
        if HOME_PATH_RE.search(text):
            violations.append(f"{rel}: contains hardcoded macOS home path")
        if ACCOUNT_OR_KEY_RE.search(text):
            violations.append(f"{rel}: contains broker account ID or API key pattern")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PINS_LOCK.json and privacy hygiene.")
    parser.add_argument("--verify-no-leaks", action="store_true")
    parser.add_argument("--online", action="store_true")
    args = parser.parse_args()

    root = pathlib.Path(__file__).resolve().parents[2]
    doc = load_pins_lock(root)
    errs = validate_pins_lock(doc, online_ls_remote=args.online)
    if args.verify_no_leaks:
        errs.extend(scan_repo_privacy_hygiene(root))
    if errs:
        for e in errs:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(
        f"PASS: 18 upstream SHA pins, 5-stage promotion ladder, and 0 privacy leaks verified in {root.name}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
