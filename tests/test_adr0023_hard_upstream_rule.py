"""Deterministic tests for ADR-0023 Universal Hard SOTA Upstream-Source & ADR-Evidence Rule."""

from __future__ import annotations

import json
import pathlib
import subprocess

from shelf_lock.hard_upstream_rule import (
    HARD_UPSTREAM_RULE_ADR,
    HARD_UPSTREAM_RULE_SCHEMA,
    audit_workstation_repos,
    parse_upstream_md_components,
    verify_adrs_have_evidence,
    verify_sealed_manifests,
    verify_shelf_pins_on_disk,
    verify_upstream_map,
)
from shelf_lock.validator import load_pins_lock

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def _init_temp_git_repo(tmp_path: pathlib.Path, files: dict[str, str]) -> pathlib.Path:
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    return tmp_path


def test_self_repo_passes_hard_upstream_rule_and_adr_evidence() -> None:
    assert verify_upstream_map(REPO_ROOT, covered_prefixes=("src/", "scripts/")) == []
    assert verify_adrs_have_evidence(REPO_ROOT) == []
    assert verify_sealed_manifests(REPO_ROOT) == []
    assert verify_shelf_pins_on_disk(load_pins_lock(REPO_ROOT)) == []


def test_parse_upstream_md_handles_tables_and_sha_bullets() -> None:
    sample = (
        "| `nautilus_trader` | v2.0.0rc9 | LGPL | https://github.com/nautechsystems/nautilus_trader | 2026 | sim | upstream |\n"
        "- `pola-rs/polars` @ `7f902bd3ffd27ff82d14278a09a295ff2f7aed92`\n"
        "| VectorBT | 1.2.0 | https://github.com/polakowo/vectorbt | 2026 | sweeps | upstream |\n"
    )
    reg = parse_upstream_md_components(sample)
    assert "nautilus_trader" in reg
    assert "polars" in reg
    assert "pola-rs/polars" in reg
    assert "VectorBT" in reg


def test_rejects_orphan_file_and_unused_pattern(tmp_path: pathlib.Path) -> None:
    repo = _init_temp_git_repo(
        tmp_path,
        {
            "UPSTREAM.md": "- `nautechsystems/nautilus_trader` @ `da6b57aefdd62b44f675e434ffcfefca7f4025dd`\n",
            "upstream-map.toml": (
                "[areas]\n"
                '"src/known.py" = { upstream = "nautilus_trader", how = "build-on", feature = "f", why = "w" }\n'
                '"src/ghost.py" = { upstream = "nautilus_trader", how = "build-on", feature = "f", why = "w" }\n'
            ),
            "src/known.py": "x = 1\n",
            "src/orphan.py": "y = 2\n",
        },
    )
    errs = verify_upstream_map(repo, covered_prefixes=("src/",))
    assert any("orphan.py" in e for e in errs)
    assert any("ghost.py" in e for e in errs)


def test_rejects_banned_low_quality_and_bespoke_sim_placeholder(tmp_path: pathlib.Path) -> None:
    repo = _init_temp_git_repo(
        tmp_path,
        {
            "UPSTREAM.md": (
                "| `yfinance` | 0.2 | Apache | url | 2026 | bad | upstream |\n"
                "| `cpython-stdlib` | 3.12 | PSF | url | 2026 | std | upstream |\n"
            ),
            "upstream-map.toml": (
                "[areas]\n"
                '"src/bad_loader.py" = { upstream = "yfinance", how = "integrate", feature = "f", why = "w" }\n'
                '"src/my_strategy_backtest.py" = { upstream = "cpython-stdlib", how = "build-on", feature = "f", why = "w" }\n'
            ),
            "src/bad_loader.py": "pass\n",
            "src/my_strategy_backtest.py": "pass\n",
        },
    )
    errs = verify_upstream_map(repo, covered_prefixes=("src/",), strict_engine_binding=True)
    assert any("banned low-quality upstream 'yfinance'" in e for e in errs)
    assert any("non-library placeholder 'cpython-stdlib'" in e for e in errs)


def test_accepts_engine_bound_to_nautilus_and_rejects_adr_without_evidence(tmp_path: pathlib.Path) -> None:
    repo = _init_temp_git_repo(
        tmp_path,
        {
            "UPSTREAM.md": "- `nautechsystems/nautilus_trader` @ `da6b57aefdd62b44f675e434ffcfefca7f4025dd`\n",
            "upstream-map.toml": (
                "[areas]\n"
                '"src/sar_strategy_sim.py" = { upstream = "nautilus_trader", how = "build-on", feature = "BacktestEngine + Strategy", why = "native SAR replay" }\n'
            ),
            "src/sar_strategy_sim.py": "pass\n",
            "docs/adr/ADR-0001-no-proof.md": "# ADR-0001: Unproven\n\nJust vibes, zero proof.\n",
            "docs/adr/ADR-0002-with-proof.md": "# ADR-0002: Proven\n\n## Verification Witness\n- pytest PASS\n",
            "docs/BAD_MANIFEST.json": json.dumps({"schema": "x"}),
            "docs/GOOD_MANIFEST.json": json.dumps({"schema": "x", "manifest_sha256": "a" * 64}),
        },
    )
    assert verify_upstream_map(repo, covered_prefixes=("src/",), strict_engine_binding=True) == []
    adr_errs = verify_adrs_have_evidence(repo)
    assert len(adr_errs) == 1 and "ADR-0001-no-proof.md" in adr_errs[0]
    man_errs = verify_sealed_manifests(repo)
    assert len(man_errs) == 1 and "BAD_MANIFEST.json" in man_errs[0]


def test_audit_workstation_repos_emits_sealed_sha256_report(tmp_path: pathlib.Path) -> None:
    sub = _init_temp_git_repo(
        tmp_path / "demo-repo",
        {
            "UPSTREAM.md": "- `nautechsystems/nautilus_trader` @ `da6b57aefdd62b44f675e434ffcfefca7f4025dd`\n",
            "upstream-map.toml": (
                "[areas]\n"
                '"src/app.py" = { upstream = "nautilus_trader", how = "build-on", feature = "engine", why = "sim" }\n'
            ),
            "src/app.py": "pass\n",
            "docs/adr/ADR-0001-demo.md": "# ADR-0001: Demo\n\n## Evidence\n- E4 verified\n",
        },
    )
    assert sub.is_dir()
    report = audit_workstation_repos(tmp_path, pins_lock=load_pins_lock(REPO_ROOT), shelf_root=tmp_path / "absent")
    assert report["schema"] == HARD_UPSTREAM_RULE_SCHEMA
    assert report["adr"] == HARD_UPSTREAM_RULE_ADR
    assert report["repos_audited"] == 1
    assert report["repos_passing_upstream_map"] == 1
    assert report["repos_passing_adr_evidence"] == 1
    assert len(report["manifest_sha256"]) == 64


def test_bootstrap_cleanroom_spl_org_generates_verified_6_repo_blueprint(tmp_path: pathlib.Path) -> None:
    from shelf_lock.hard_upstream_rule import bootstrap_cleanroom_spl_org, parse_upstream_md_components

    out = bootstrap_cleanroom_spl_org(tmp_path / "spl-org", org_name="sota-spl-demo")
    assert out["repos_count"] == 6
    assert out["shelf_pins_count"] == 18
    assert len(out["manifest_sha256"]) == 64
    assert (tmp_path / "spl-org" / "ORG_BLUEPRINT_MANIFEST.json").is_file()
    for row in out["repos"]:
        rdir = tmp_path / "spl-org" / row["repo"]
        assert (rdir / "UPSTREAM.md").is_file()
        assert (rdir / "upstream-map.toml").is_file()
        assert (rdir / "scripts" / "merge_gate.py").is_file()
        assert (rdir / "orca.yaml").is_file()
    comps = parse_upstream_md_components(
        "| **L0** | `mise` | https://github.com/jdx/mise | `2026.11.6` | MIT |"
    )
    assert "mise" in comps and "jdx/mise" in comps
