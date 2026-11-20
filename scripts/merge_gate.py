#!/usr/bin/env python3
"""Fail-Closed Merge Gate for `sota-upstream-shelf-lock` (`ADR-0023`)."""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from shelf_lock.hard_upstream_rule import (
    verify_adrs_have_evidence,
    verify_sealed_manifests,
    verify_shelf_pins_on_disk,
    verify_upstream_map,
    verify_zero_leaks_and_noreply,
)
from shelf_lock.validator import load_pins_lock, validate_pins_lock


def main() -> int:
    problems: list[str] = []
    problems.extend(validate_pins_lock(load_pins_lock(ROOT)))
    problems.extend(verify_upstream_map(ROOT, covered_prefixes=("src/", "scripts/")))
    problems.extend(verify_adrs_have_evidence(ROOT))
    problems.extend(verify_sealed_manifests(ROOT))
    problems.extend(verify_shelf_pins_on_disk(load_pins_lock(ROOT)))
    problems.extend(verify_zero_leaks_and_noreply(ROOT))

    cat = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "architecture_catalog.py"), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    if cat.returncode != 0:
        problems.append(f"ADR catalog drift: {cat.stderr.strip() or cat.stdout.strip()}")

    if problems:
        for p in problems:
            print(f"[MERGE-GATE FAIL] {p}", file=sys.stderr)
        return 1

    print("[MERGE-GATE PASS] ADR-0023 upstream-map, 18-pin shelf, ADR evidence, PINS_LOCK, and zero-leak verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
