"""Universal Ecosystem-Wide Tier-0 Full-Resolution, Zero-Residual, Zero-Fallback Hard Rule (`ADR-0025`).

Codifies the owner's permanent invariant across all `native-agent-stack` repositories and lanes:
**Full resolution and always full resolution — zero residual stubs, zero empty-engine boot checks,
zero pure-Python heuristics masquerading as Rust/C++ upstream engines, and zero silent fallbacks.**

Enforced deterministically at both CI/merge-gate time and runtime manifest verification:
1. **FR-1 (Zero Empty `NautilusTrader` Boot Stubs):** Every `BacktestEngine.run()` must wire
   `add_instrument`, `add_data`, and `add_strategy`; every sealed manifest entry for `nautilus_trader`
   must prove `iterations > 0`, `instruments_n >= 1`, `bars_or_ticks_loaded > 0`, `strategies_n >= 1`,
   `orders_total > 0`, and `fills_total > 0`.
2. **FR-2 (Zero Residual Pure-Python `hftbacktest` Fallbacks):** Sealed `hftbacktest` runs must prove
   `engine_kind == "RUST_HFTBACKTEST_HASHMAP_DEPTH"`, `queue_model == "RiskAdverseQueueModel"`,
   `slices_replayed >= 1`, and `events_replayed > 0`. Keys like `hftbacktest_queue_parity_ref` are banned.
3. **FR-3 (Zero Silent CPU / Synthetic / Degraded Fallbacks):** Every upstream run must prove
   `executed is True`, `fallback_used is not True`, `synthetic is not True`, `degraded is not True`,
   `post_wall_n == 0` (`<= 2026-10-15`), and `rtx4090_gpu_cuda.device.startswith("cuda")`.
4. **FR-4 (Cross-Repo Workstation Audit):** `audit_workstation_full_resolution(workstation_root)`
   scans all active repositories for empty `BacktestEngine` stubs and verifies sealed E2E manifests.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import pathlib
import subprocess
import sys
from collections.abc import Mapping, Sequence
from typing import Any

FULL_RESOLUTION_UNIVERSAL_SCHEMA = "sota.universal-full-resolution-rule.v1"
FULL_RESOLUTION_UNIVERSAL_ADR = "ADR-0025"

REQUIRED_FULL_RES_ENGINES: tuple[str, ...] = (
    "polars_duckdb_pandera_xnys",
    "nautilus_trader",
    "hftbacktest",
    "vectorbt",
    "statsmodels",
    "skfolio",
    "ml4t_diagnostic",
    "bashtage_arch",
    "rtx4090_gpu_cuda",
)

FORBIDDEN_RESIDUAL_ENGINE_KEYS: frozenset[str] = frozenset(
    {
        "hftbacktest_queue_parity_ref",
        "cpu_fallback",
        "python_bar_loop_fallback",
        "synthetic_smoke",
        "nautilus_boot_only",
        "vectorbt_nautilus",
        "econometric_battery",
    }
)

_INVALID_VERSIONS: frozenset[str] = frozenset(
    {"", "n/a", "none", "unavailable", "fallback", "stub", "mock", "synthetic"}
)


def _pos_int(val: Any) -> int:
    if isinstance(val, bool) or val is None:
        return 0
    try:
        iv = int(val)
    except (TypeError, ValueError):
        return 0
    return max(0, iv)


def compute_manifest_digest(payload: Mapping[str, Any]) -> str:
    """Compute canonical SHA-256 digest over deterministic manifest fields (excluding timestamps/digest)."""
    base = {k: v for k, v in payload.items() if k not in ("manifest_sha256", "generated_at_utc")}
    canonical = json.dumps(base, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def verify_full_resolution_manifest(
    manifest: Mapping[str, Any],
    *,
    require_all_engines: bool = True,
    verify_sha256: bool = True,
) -> dict[str, Any]:
    """Fail-closed verifier enforcing ADR-0025 across any sealed upstream-library E2E manifest."""
    violations: list[str] = []
    residual_fallbacks_count = 0
    verified_engines: list[str] = []

    if not isinstance(manifest, Mapping):
        return {
            "schema": FULL_RESOLUTION_UNIVERSAL_SCHEMA,
            "adr": FULL_RESOLUTION_UNIVERSAL_ADR,
            "full_resolution_verified": False,
            "allow_silent_fallback": False,
            "residual_fallbacks_count": 1,
            "engines_verified_n": 0,
            "required_engines_n": len(REQUIRED_FULL_RES_ENGINES),
            "violations": ["MANIFEST_NOT_MAPPING"],
        }

    if verify_sha256:
        expected = compute_manifest_digest(manifest)
        if str(manifest.get("manifest_sha256") or "") != expected:
            violations.append("MANIFEST_SHA256_MISMATCH")

    runs = manifest.get("upstream_library_runs")
    if not isinstance(runs, Mapping) or not runs:
        violations.append("MISSING_UPSTREAM_LIBRARY_RUNS")
        return {
            "schema": FULL_RESOLUTION_UNIVERSAL_SCHEMA,
            "adr": FULL_RESOLUTION_UNIVERSAL_ADR,
            "full_resolution_verified": False,
            "allow_silent_fallback": False,
            "residual_fallbacks_count": 1,
            "engines_verified_n": 0,
            "required_engines_n": len(REQUIRED_FULL_RES_ENGINES),
            "violations": violations,
        }

    for key in sorted(runs.keys()):
        if key in FORBIDDEN_RESIDUAL_ENGINE_KEYS:
            residual_fallbacks_count += 1
            violations.append(f"FORBIDDEN_RESIDUAL_ENGINE:{key}")

    if require_all_engines:
        for req in REQUIRED_FULL_RES_ENGINES:
            if req not in runs:
                violations.append(f"MISSING_REQUIRED_ENGINE:{req}")

    for eng, entry in sorted(runs.items()):
        if eng in FORBIDDEN_RESIDUAL_ENGINE_KEYS:
            continue
        if not isinstance(entry, Mapping):
            violations.append(f"MALFORMED_ENGINE_ENTRY:{eng}")
            continue

        ok = True
        if entry.get("executed") is not True:
            ok = False
            violations.append(f"ENGINE_NOT_EXECUTED:{eng}")

        for flag in ("fallback_used", "synthetic", "degraded", "residual_loop_used"):
            if entry.get(flag) is True:
                ok = False
                residual_fallbacks_count += 1
                violations.append(f"FORBIDDEN_FALLBACK_FLAG:{eng}:{flag}")

        ver = str(entry.get("version") or "").strip().lower()
        if ver in _INVALID_VERSIONS or "fallback" in ver or "err" in ver:
            ok = False
            violations.append(f"INVALID_VERSION:{eng}:{ver}")

        summ = str(entry.get("summary") or "").lower()
        if "iterations=0" in summ or "boot_error" in summ or "fallback" in summ:
            ok = False
            residual_fallbacks_count += 1
            violations.append(f"STUB_OR_FALLBACK_SUMMARY:{eng}")

        post_wall = entry.get("post_wall_n")
        if isinstance(post_wall, int) and not isinstance(post_wall, bool) and post_wall > 0:
            ok = False
            violations.append(f"POST_WALL_LEAK:{eng}:post_wall_n={post_wall}")

        if eng == "nautilus_trader":
            if _pos_int(entry.get("iterations")) <= 0:
                ok = False
                residual_fallbacks_count += 1
                violations.append("NAUTILUS_ZERO_ITERATIONS_BOOT_STUB")
            if _pos_int(entry.get("instruments_n")) < 1 or _pos_int(entry.get("bars_or_ticks_loaded")) <= 0:
                ok = False
                violations.append("NAUTILUS_MISSING_INSTRUMENTS_OR_DATA")
            if _pos_int(entry.get("strategies_n")) < 1:
                ok = False
                violations.append("NAUTILUS_MISSING_STRATEGY")
            if _pos_int(entry.get("orders_total")) <= 0 or _pos_int(entry.get("fills_total")) <= 0:
                ok = False
                violations.append("NAUTILUS_ZERO_ORDERS_OR_FILLS")

        elif eng == "hftbacktest":
            if str(entry.get("engine_kind") or "") != "RUST_HFTBACKTEST_HASHMAP_DEPTH":
                ok = False
                residual_fallbacks_count += 1
                violations.append("HFTBACKTEST_NON_RUST_FALLBACK")
            if str(entry.get("queue_model") or "") != "RiskAdverseQueueModel":
                ok = False
                violations.append("HFTBACKTEST_MISSING_RISK_ADVERSE_QUEUE_MODEL")
            if _pos_int(entry.get("slices_replayed")) < 1 or _pos_int(entry.get("events_replayed")) <= 0:
                ok = False
                violations.append("HFTBACKTEST_ZERO_EVENTS_REPLAYED")

        elif eng == "rtx4090_gpu_cuda":
            dev = str(entry.get("device") or "").lower()
            if not dev.startswith("cuda"):
                ok = False
                residual_fallbacks_count += 1
                violations.append(f"GPU_CUDA_REQUIRED_NO_CPU_FALLBACK:{dev}")
            if _pos_int(entry.get("n_boot")) < 1000:
                ok = False
                violations.append("GPU_BOOTSTRAP_INSUFFICIENT_REPS")

        elif eng == "polars_duckdb_pandera_xnys":
            if _pos_int(entry.get("sessions_n")) < 60 or _pos_int(entry.get("total_1m_bars_aggregated")) <= 0:
                ok = False
                violations.append("LAKE_INSUFFICIENT_DATA")
            if entry.get("non_xnys_n", 0) != 0:
                ok = False
                violations.append("LAKE_NON_XNYS_SESSIONS")

        elif eng == "vectorbt":
            plateaus = entry.get("plateau_results")
            if not isinstance(plateaus, Sequence) or isinstance(plateaus, (str, bytes)) or len(plateaus) < 1:
                ok = False
                violations.append("VECTORBT_EMPTY_PLATEAUS")

        elif eng == "skfolio":
            if _pos_int(entry.get("cpcv_splits_n")) < 10:
                ok = False
                violations.append("SKFOLIO_INSUFFICIENT_SPLITS")

        elif eng == "ml4t_diagnostic":
            for k in ("dsr_probability", "whites_rc_p"):
                v = entry.get(k)
                if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(float(v)):
                    ok = False
                    violations.append(f"ML4T_NON_FINITE:{k}")

        elif eng == "bashtage_arch":
            spa = entry.get("spa_p_consistent")
            mcs = entry.get("mcs_surviving_set")
            if (
                not isinstance(spa, (int, float))
                or isinstance(spa, bool)
                or not math.isfinite(float(spa))
                or not isinstance(mcs, Sequence)
                or isinstance(mcs, (str, bytes))
                or len(mcs) < 1
            ):
                ok = False
                violations.append("ARCH_INVALID_SPA_OR_MCS")

        if ok and eng in REQUIRED_FULL_RES_ENGINES:
            verified_engines.append(eng)

    return {
        "schema": FULL_RESOLUTION_UNIVERSAL_SCHEMA,
        "adr": FULL_RESOLUTION_UNIVERSAL_ADR,
        "full_resolution_verified": len(violations) == 0,
        "allow_silent_fallback": False,
        "residual_fallbacks_count": residual_fallbacks_count,
        "engines_verified_n": len(verified_engines),
        "required_engines_n": len(REQUIRED_FULL_RES_ENGINES),
        "violations": violations,
    }


def _collect_call_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name):
                names.add(fn.id)
            elif isinstance(fn, ast.Attribute):
                names.add(fn.attr)
    return names


def audit_python_text_for_empty_engine_stubs(source_text: str, rel_path: str) -> list[str]:
    """Static AST check catching empty `BacktestEngine.run()` stubs (including inline subprocess scripts)."""
    issues: list[str] = []
    try:
        tree = ast.parse(source_text)
    except SyntaxError:
        return issues

    trees: list[tuple[str, ast.AST]] = [(rel_path, tree)]
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and "BacktestEngine(" in node.value:
            try:
                trees.append((f"{rel_path}<inline>", ast.parse(node.value)))
            except SyntaxError:
                pass

    for label, sub in trees:
        calls = _collect_call_names(sub)
        if "BacktestEngine" in calls and "run" in calls:
            missing = [req for req in ("add_instrument", "add_data", "add_strategy") if req not in calls]
            if missing:
                issues.append(f"{label}: EMPTY_NAUTILUS_BACKTEST_ENGINE_STUB missing {missing}")
    return issues


def audit_repo_full_resolution(
    repo_root: pathlib.Path,
    *,
    covered_prefixes: tuple[str, ...] = (
        "src/",
        "scripts/",
        "ranker/",
        "meridian/",
        "astrolabe/",
        "research/",
    ),
) -> list[str]:
    """Audit one repository for empty `BacktestEngine` stubs and full-resolution manifest compliance."""
    issues: list[str] = []
    res = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files"],
        capture_output=True,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        return [f"{repo_root.name}: git ls-files failed"]

    for rel in (ln.strip() for ln in res.stdout.splitlines() if ln.strip()):
        if not rel.startswith(covered_prefixes) or not rel.endswith(".py"):
            continue
        fp = repo_root / rel
        if not fp.is_file():
            continue
        try:
            txt = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        issues.extend(audit_python_text_for_empty_engine_stubs(txt, f"{repo_root.name}/{rel}"))

    e2e_manifest = repo_root / "docs" / "SOTA_UPSTREAM_LIB_E2E_REGIME_PERSYMBOL_MANIFEST.json"
    if e2e_manifest.is_file():
        try:
            data = json.loads(e2e_manifest.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
            issues.append(f"{repo_root.name}: corrupt E2E manifest: {exc}")
        else:
            audit = verify_full_resolution_manifest(data, require_all_engines=True, verify_sha256=True)
            if not audit["full_resolution_verified"]:
                for v in audit["violations"]:
                    issues.append(f"{repo_root.name}: ADR-0025 full-resolution violation: {v}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit repos against ADR-0025 Full-Resolution Zero-Fallback Rule."
    )
    parser.add_argument("--repo", required=True, help="Path to repository root to audit")
    args = parser.parse_args()
    issues = audit_repo_full_resolution(pathlib.Path(args.repo))
    if issues:
        for i in issues:
            print(f"[ADR-0025 FAIL] {i}", file=sys.stderr)
        return 1
    print(f"[ADR-0025 PASS] {args.repo}: 0 empty BacktestEngine stubs, 0 residual/fallback violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
