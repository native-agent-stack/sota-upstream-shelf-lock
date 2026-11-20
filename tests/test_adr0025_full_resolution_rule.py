"""Tests for ADR-0025: Universal Full-Resolution, Zero-Residual, Zero-Fallback Hard Rule."""

from __future__ import annotations

import json
import pathlib
from typing import Any

from shelf_lock.full_resolution_rule import (
    FORBIDDEN_RESIDUAL_ENGINE_KEYS,
    REQUIRED_FULL_RES_ENGINES,
    audit_python_text_for_empty_engine_stubs,
    audit_repo_full_resolution,
    compute_manifest_digest,
    verify_full_resolution_manifest,
)


def _valid_manifest() -> dict[str, Any]:
    runs: dict[str, Any] = {
        "polars_duckdb_pandera_xnys": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "polars 2.1.0 / duckdb 2.0.0",
            "sessions_n": 700,
            "total_1m_bars_aggregated": 7_836_606,
            "non_xnys_n": 0,
            "post_wall_n": 0,
            "summary": "700 official XNYS sessions",
        },
        "nautilus_trader": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "2.0.0rc9",
            "instruments_n": 15,
            "bars_or_ticks_loaded": 10_500,
            "strategies_n": 1,
            "iterations": 10_500,
            "orders_total": 654,
            "fills_total": 590,
            "summary": "15 Equity instruments, 10,500 iterations, 590 fills",
        },
        "hftbacktest": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "engine_kind": "RUST_HFTBACKTEST_HASHMAP_DEPTH",
            "queue_model": "RiskAdverseQueueModel",
            "version": "2.4.2",
            "slices_replayed": 12,
            "events_replayed": 1_138_548,
            "post_wall_n": 0,
            "summary": "Rust hftbacktest v2.4.2 RiskAdverseQueueModel",
        },
        "vectorbt": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "1.2.0",
            "plateau_results": [{"config": "VBT_20D_BREAKOUT"}],
            "summary": "4 plateau sweeps",
        },
        "statsmodels": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "0.15.0",
            "summary": "OLS HAC",
        },
        "skfolio": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "1.12.7",
            "cpcv_splits_n": 15,
            "summary": "CPCV C(6,2)=15",
        },
        "ml4t_diagnostic": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "0.2.0",
            "dsr_probability": 0.0065,
            "whites_rc_p": 0.0775,
            "summary": "DSR/WRC",
        },
        "bashtage_arch": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "9.0.0",
            "spa_p_consistent": 0.052,
            "mcs_surviving_set": ["VBT_20D_BREAKOUT"],
            "summary": "SPA/MCS",
        },
        "rtx4090_gpu_cuda": {
            "executed": True,
            "synthetic": False,
            "fallback_used": False,
            "version": "torch-cuda / RTX 4090",
            "device": "cuda:0",
            "n_boot": 10_000,
            "summary": "RTX 4090 cuda:0 10,000-rep bootstrap",
        },
    }
    m: dict[str, Any] = {"schema": "test", "upstream_library_runs": runs}
    m["manifest_sha256"] = compute_manifest_digest(m)
    return m


def test_adr0025_passes_full_resolution_9_engine_manifest_and_live_compounding_lab() -> None:
    res = verify_full_resolution_manifest(_valid_manifest())
    assert res["full_resolution_verified"] is True
    assert res["allow_silent_fallback"] is False
    assert res["residual_fallbacks_count"] == 0
    assert res["engines_verified_n"] == len(REQUIRED_FULL_RES_ENGINES)

    compounding_root = pathlib.Path(__file__).resolve().parents[2] / "sota-compounding-lab"
    if compounding_root.is_dir():
        issues = audit_repo_full_resolution(compounding_root)
        assert issues == [], f"Unexpected full-resolution violations in sota-compounding-lab: {issues}"


def test_adr0025_rejects_empty_nautilus_stub_and_python_hft_residual() -> None:
    m = _valid_manifest()
    m["upstream_library_runs"]["nautilus_trader"]["iterations"] = 0
    m["upstream_library_runs"]["hftbacktest_queue_parity_ref"] = {
        "executed": True,
        "version": "ref",
        "summary": "ref",
    }
    m["manifest_sha256"] = compute_manifest_digest(m)
    res = verify_full_resolution_manifest(m)
    assert res["full_resolution_verified"] is False
    assert "NAUTILUS_ZERO_ITERATIONS_BOOT_STUB" in res["violations"]
    assert "FORBIDDEN_RESIDUAL_ENGINE:hftbacktest_queue_parity_ref" in res["violations"]


def test_adr0025_ast_catches_inline_empty_backtest_engine() -> None:
    src = 'code = """\ne = BacktestEngine(cfg)\ne.add_venue(v)\ne.run()\n"""\n'
    issues = audit_python_text_for_empty_engine_stubs(src, "scripts/stub.py")
    assert len(issues) == 1
    assert "EMPTY_NAUTILUS_BACKTEST_ENGINE_STUB" in issues[0]


def test_exhaustive_matrix_no_residual_cpu_stub_or_postwall_passes_adr0025() -> None:
    for forbidden_key in sorted(FORBIDDEN_RESIDUAL_ENGINE_KEYS):
        m1 = _valid_manifest()
        m1["upstream_library_runs"][forbidden_key] = {"executed": True, "version": "1.0", "summary": "x"}
        m1["manifest_sha256"] = compute_manifest_digest(m1)
        out1 = verify_full_resolution_manifest(m1)
        assert out1["full_resolution_verified"] is False
        assert out1["residual_fallbacks_count"] >= 1
        json.dumps(out1, allow_nan=False)

    for bad_dev in ("cpu", "python-cpu", "mps", ""):
        m2 = _valid_manifest()
        m2["upstream_library_runs"]["rtx4090_gpu_cuda"]["device"] = bad_dev
        m2["manifest_sha256"] = compute_manifest_digest(m2)
        out2 = verify_full_resolution_manifest(m2)
        assert out2["full_resolution_verified"] is False
        assert out2["residual_fallbacks_count"] >= 1
        json.dumps(out2, allow_nan=False)

    for bad_iters in (-5, -1, 0):
        m3 = _valid_manifest()
        m3["upstream_library_runs"]["nautilus_trader"]["iterations"] = bad_iters
        m3["manifest_sha256"] = compute_manifest_digest(m3)
        assert verify_full_resolution_manifest(m3)["full_resolution_verified"] is False

    m4 = _valid_manifest()
    m4["upstream_library_runs"]["polars_duckdb_pandera_xnys"]["post_wall_n"] = 1
    m4["manifest_sha256"] = compute_manifest_digest(m4)
    assert verify_full_resolution_manifest(m4)["full_resolution_verified"] is False
