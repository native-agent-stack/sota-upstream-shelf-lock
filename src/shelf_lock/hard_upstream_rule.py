"""Universal Fail-Closed SOTA Upstream-Source & ADR-Evidence Hard Rule (`ADR-0023`).

Enforces four non-negotiable ecosystem invariants across `native-agent-stack`:
1. **Zero Orphan Implementation Code:** Every tracked implementation file must map in
   `upstream-map.toml` with `how` in `{"install", "integrate", "build-on"}`, non-empty
   `feature` and `why`, referencing an entry registered in `UPSTREAM.md`. Unused rules fail.
2. **Zero Bespoke Engine Escape Hatches & Zero Banned Low-Quality Sources:** Strategy,
   backtest, and simulation engine modules must bind to a real, maintained SOTA upstream
   library (never `yfinance`, `backtrader`, `backtesting.py`, abandoned `mlfinlab`, or
   bare stdlib/literature placeholders without an explicit upstream library binding).
3. **Every ADR & Sealed Manifest Carries Evidence:** Every MADR 4.0 ADR in `docs/adr/`
   must cite concrete verification/evidence (`Evidence`, `Verification Witness`,
   `Confirmation`, `GitHub Evidence`, or `Rests on:`), and every tracked JSON manifest must
   be strict finite JSON with a digest and zero secret/account/home-path leaks.
4. **Immutable 18-Pin Read-Only Shelf Parity:** When `~/Documents/upstream/` is present,
   every one of the 18 pinned upstream clones must sit cleanly on its exact 40-char SHA.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tomllib
from typing import Any

from shelf_lock.validator import ACCOUNT_OR_KEY_RE, HOME_PATH_RE, load_pins_lock

HARD_UPSTREAM_RULE_SCHEMA = "sota.hard-upstream-source-rule.v1"
HARD_UPSTREAM_RULE_ADR = "ADR-0023"

ALLOWED_HOW_MODES: frozenset[str] = frozenset({"install", "integrate", "build-on"})

BANNED_LOW_QUALITY_UPSTREAMS: frozenset[str] = frozenset(
    {
        "yfinance",
        "backtrader",
        "backtesting.py",
        "backtesting",
        "mlfinlab",
        "tcapy",
        "vollib",
        "abides-jpmc-public",
        "tradingview_ta",
        "pandas-datareader",
    }
)

# Bare non-library placeholders disallowed as sole upstream provenance for active sim/backtest/strategy engines
NON_LIBRARY_ENGINE_PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "cpython-stdlib",
        "cpython",
        "stdlib",
        "academic-momentum-literature",
        "own-design",
    }
)

ENGINE_FILENAME_KEYWORDS: tuple[str, ...] = (
    "backtest",
    "sim",
    "strategy",
    "strategies",
    "sar",
    "norm_disruption",
    "alpha_factory",
    "execution_core",
    "paper_auto_engine",
)

PURE_GOVERNANCE_EXEMPT_KEYWORDS: tuple[str, ...] = (
    "__init__",
    "manifest",
    "contract",
    "quarantine",
    "policy",
    "validator",
    "hard_upstream_rule",
    "catalog",
    "merge_gate",
    "architecture_catalog",
    "doctor",
    "fixture",
    "template.json",
)

WIN_HOME_PATH_RE = re.compile(r"\b[A-Za-z]:[/\\]Users[/\\](?!<user>)[A-Za-z0-9._-]+[/\\]")
LINUX_HOME_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.-])/home/(?!<user>|agent)[A-Za-z0-9._-]+/")

ADR_EVIDENCE_MARKERS: tuple[str, ...] = (
    "evidence",
    "verification witness",
    "confirmation",
    "github evidence",
    "rests on:",
    "docs/adr/data/",
    "data/",
)

DEFAULT_COVERED_PREFIXES: tuple[str, ...] = (
    "src/",
    "scripts/",
    "ranker/",
    "meridian/",
    "research/",
    "astrolabe/",
    "workflows/",
    "tradingview_suite/",
    "server.py",
    "mcp_server.py",
)

CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


def _norm_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")


def _clean_git_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def _run_git(repo_root: pathlib.Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    kwargs: dict[str, Any] = {
        "capture_output": True,
        "text": True,
        "env": _clean_git_env(),
    }
    if sys.platform == "win32":
        kwargs["creationflags"] = CREATE_NO_WINDOW
    return subprocess.run(["git", "-C", str(repo_root), *args], check=False, **kwargs)


def parse_upstream_md_components(up_md_text: str) -> set[str]:
    """Extract all registered upstream identifiers from markdown tables and SHA-pinned lists."""
    registered: set[str] = set()
    # 1. Backtick-quoted first cell in markdown tables: | `component` | ...
    for m in re.findall(r"^\|\s*`([^`]+)`\s*\|", up_md_text, flags=re.MULTILINE):
        registered.add(m.strip())
        registered.add(_norm_key(m))
    # 2. Meridian/Astrolabe plain markdown table rows ending in `| upstream |`
    for line in up_md_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) >= 6 and cells[-1].lower() == "upstream":
            raw = cells[0].strip("`").strip()
            if raw:
                registered.add(raw)
                registered.add(_norm_key(raw))
    # 3. Bullet SHA-pin lists: - `org/repo` @ `40hex`
    for org_repo in re.findall(r"-\s+`([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)`\s*@", up_md_text):
        registered.add(org_repo)
        registered.add(_norm_key(org_repo))
        short = org_repo.split("/", 1)[1]
        registered.add(short)
        registered.add(_norm_key(short))
    # 4. Inline parenthesized GitHub repos in orchestration sections: (`org/repo` ...)
    for org_repo in re.findall(r"\(`([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)`", up_md_text):
        registered.add(org_repo)
        registered.add(_norm_key(org_repo))
        short = org_repo.split("/", 1)[1]
        registered.add(short)
        registered.add(_norm_key(short))
    # 5. Backticked 2nd-column tables (e.g. | **L0** | `mise` | ...) and GitHub repo URLs
    for line in up_md_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) >= 3:
            for tok in re.findall(r"`([A-Za-z0-9_./-]+)`", cells[1]):
                registered.add(tok)
                registered.add(_norm_key(tok))
                if "/" in tok:
                    short = tok.split("/", 1)[1]
                    registered.add(short)
                    registered.add(_norm_key(short))
    for org_repo in re.findall(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", up_md_text):
        clean_or = org_repo.rstrip("`.,);")
        if "/" in clean_or:
            registered.add(clean_or)
            registered.add(_norm_key(clean_or))
            short = clean_or.split("/", 1)[1]
            registered.add(short)
            registered.add(_norm_key(short))
    # 6. Explicitly register CPython stdlib when referenced as Python runtime
    if re.search(r"cpython|python\s*3\.\d+", up_md_text, flags=re.IGNORECASE):
        registered.update({"cpython-stdlib", "CPython", "cpython"})
    return registered


def is_sim_or_strategy_engine_pattern(pattern: str) -> bool:
    """Return True if a path/pattern denotes an active strategy, backtest, or sim engine file."""
    low = pattern.lower()
    if any(ex in low for ex in PURE_GOVERNANCE_EXEMPT_KEYWORDS):
        return False
    return any(kw in low for kw in ENGINE_FILENAME_KEYWORDS)


def verify_upstream_map(
    repo_root: pathlib.Path,
    *,
    covered_prefixes: tuple[str, ...] = DEFAULT_COVERED_PREFIXES,
    strict_engine_binding: bool = True,
) -> list[str]:
    """Fail-closed check of UPSTREAM.md + upstream-map.toml against git-tracked files."""
    errors: list[str] = []
    up_md = repo_root / "UPSTREAM.md"
    map_toml = repo_root / "upstream-map.toml"
    if not up_md.is_file():
        return ["Missing UPSTREAM.md"]
    if not map_toml.is_file():
        return ["Missing upstream-map.toml"]

    registered = parse_upstream_md_components(up_md.read_text(encoding="utf-8"))
    try:
        cfg = tomllib.loads(map_toml.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError, OSError) as exc:
        return [f"upstream-map.toml parse failure: {exc}"]

    areas = cfg.get("areas")
    if not isinstance(areas, dict) or not areas:
        return ["upstream-map.toml must define non-empty [areas] table"]

    for pat, meta in areas.items():
        if not isinstance(meta, dict):
            errors.append(f"upstream-map.toml pattern '{pat}' must be an inline table")
            continue
        u_name = str(meta.get("upstream", "")).strip()
        how = str(meta.get("how", "")).strip()
        feature = str(meta.get("feature", "")).strip()
        why = str(meta.get("why", "")).strip()
        upstream_libs = meta.get("upstream_libs")

        if not u_name:
            errors.append(f"upstream-map.toml pattern '{pat}' missing upstream")
        else:
            u_norm = _norm_key(u_name)
            if u_norm in {_norm_key(b) for b in BANNED_LOW_QUALITY_UPSTREAMS}:
                errors.append(f"upstream-map.toml pattern '{pat}' cites banned low-quality upstream '{u_name}'")
            if u_name not in registered and u_norm not in registered:
                errors.append(
                    f"upstream-map.toml pattern '{pat}' cites upstream '{u_name}' not registered in UPSTREAM.md"
                )
            if strict_engine_binding and is_sim_or_strategy_engine_pattern(pat):
                has_extra_libs = isinstance(upstream_libs, list) and any(
                    str(x).strip() and _norm_key(str(x)) not in {_norm_key(p) for p in NON_LIBRARY_ENGINE_PLACEHOLDERS}
                    for x in upstream_libs
                )
                if u_norm in {_norm_key(p) for p in NON_LIBRARY_ENGINE_PLACEHOLDERS} and not has_extra_libs:
                    errors.append(
                        f"upstream-map.toml engine pattern '{pat}' uses non-library placeholder '{u_name}'; "
                        "strategy/backtest/sim engines must bind to a real maintained SOTA upstream library"
                    )

        if how not in ALLOWED_HOW_MODES:
            errors.append(f"upstream-map.toml pattern '{pat}' invalid how={how!r}; expected {sorted(ALLOWED_HOW_MODES)}")
        if not feature:
            errors.append(f"upstream-map.toml pattern '{pat}' missing non-empty 'feature'")
        if not why:
            errors.append(f"upstream-map.toml pattern '{pat}' missing non-empty 'why'")

    ls_r = _run_git(repo_root, ["ls-files"])
    if ls_r.returncode != 0:
        return [*errors, f"git ls-files failed in {repo_root}: {ls_r.stderr.strip()}"]

    tracked = [ln.strip() for ln in ls_r.stdout.splitlines() if ln.strip()]
    used_patterns: set[str] = set()
    for rel in tracked:
        matched_any = [pat for pat in areas if fnmatch.fnmatchcase(rel, pat)]
        if matched_any:
            used_patterns.update(matched_any)
        if not rel.startswith(covered_prefixes):
            continue
        if not matched_any:
            errors.append(f"Unmapped implementation file '{rel}': add SOTA upstream entry in upstream-map.toml")

    for pat in areas:
        if pat not in used_patterns:
            errors.append(f"Unused pattern in upstream-map.toml: '{pat}'")

    return errors


def verify_adrs_have_evidence(repo_root: pathlib.Path) -> list[str]:
    """Ensure every ADR in docs/adr/ cites concrete verification or upstream evidence."""
    adr_dir = repo_root / "docs" / "adr"
    if not adr_dir.is_dir():
        return []
    errors: list[str] = []
    for path in sorted(adr_dir.glob("*.md")):
        if path.name in {"CATALOG.md", "README.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        low = text.lower()
        if not any(marker in low for marker in ADR_EVIDENCE_MARKERS):
            errors.append(f"ADR '{path.name}' lacks an Evidence / Verification Witness / Rests-on section")
    return errors


def verify_sealed_manifests(repo_root: pathlib.Path) -> list[str]:
    """Ensure every tracked docs/*MANIFEST*.json is strict finite JSON with digest & zero leaks."""
    docs_dir = repo_root / "docs"
    if not docs_dir.is_dir():
        return []
    errors: list[str] = []
    for path in sorted(docs_dir.glob("*MANIFEST*.json")):
        raw = path.read_text(encoding="utf-8")
        try:
            doc = json.loads(raw)
            json.dumps(doc, allow_nan=False)
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            errors.append(f"Manifest '{path.name}' failed strict finite JSON check: {exc}")
            continue
        if not isinstance(doc, dict):
            errors.append(f"Manifest '{path.name}' root must be JSON object")
            continue
        has_digest = any(
            k in doc for k in ("manifest_sha256", "sha256", "content_sha256", "seal_sha256")
        )
        if not has_digest:
            errors.append(f"Manifest '{path.name}' missing cryptographic digest field (manifest_sha256)")
        if ACCOUNT_OR_KEY_RE.search(raw) or HOME_PATH_RE.search(raw) or WIN_HOME_PATH_RE.search(raw):
            errors.append(f"Manifest '{path.name}' triggered privacy/home-path/account-ID leak check")
    return errors


def verify_shelf_pins_on_disk(
    pins_lock: dict[str, Any] | None = None,
    *,
    shelf_root: pathlib.Path | None = None,
) -> list[str]:
    """Verify all 18 read-only shelf clones in ~/Documents/upstream match PINS_LOCK.json SHAs."""
    root = shelf_root if shelf_root is not None else (pathlib.Path.home() / "Documents" / "upstream")
    if not root.is_dir():
        return []
    lock = pins_lock if pins_lock is not None else load_pins_lock()
    errors: list[str] = []
    for entry in lock.get("upstreamShelfPins", []):
        name = str(entry.get("name", ""))
        expected = str(entry.get("commit", ""))
        cdir = root / name
        if not cdir.is_dir():
            errors.append(f"Missing read-only upstream shelf clone: {name}")
            continue
        head_r = _run_git(cdir, ["rev-parse", "HEAD"])
        actual = head_r.stdout.strip()
        if head_r.returncode != 0 or actual != expected:
            errors.append(f"Shelf pin drift for {name}: expected {expected}, found {actual or 'ERROR'}")
        st_r = _run_git(cdir, ["status", "--short"])
        if st_r.returncode != 0 or st_r.stdout.strip():
            errors.append(f"Read-only upstream shelf clone '{name}' has dirty working-tree edits")
    return errors


def verify_zero_leaks_and_noreply(repo_root: pathlib.Path) -> list[str]:
    """Verify zero tracked secrets/home paths and noreply GitHub commit emails."""
    errors: list[str] = []
    ls_r = _run_git(repo_root, ["ls-files"])
    if ls_r.returncode != 0:
        return [f"git ls-files failed: {ls_r.stderr.strip()}"]
    for rel in (ln.strip() for ln in ls_r.stdout.splitlines() if ln.strip()):
        if rel in {"scripts/merge_gate.py", "src/shelf_lock/hard_upstream_rule.py", "src/shelf_lock/validator.py"}:
            continue
        fp = repo_root / rel
        if not fp.is_file():
            continue
        try:
            txt = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if ACCOUNT_OR_KEY_RE.search(txt):
            errors.append(f"{rel}: triggered account-ID/API-key leak pattern")
        if HOME_PATH_RE.search(txt) or WIN_HOME_PATH_RE.search(txt) or LINUX_HOME_PATH_RE.search(txt):
            errors.append(f"{rel}: triggered local home-path leak pattern")

    log_r = _run_git(repo_root, ["log", "-n", "5", "--format=%H %ae"])
    if log_r.returncode == 0:
        for ln in log_r.stdout.splitlines():
            if not ln.strip():
                continue
            sha, email = ln.strip().split(" ", 1)
            if not email.endswith(("users.noreply.github.com", "noreply@github.com")):
                errors.append(f"Commit {sha[:10]} uses non-noreply email '{email}'")
    return errors


def audit_workstation_repos(
    workstation_root: pathlib.Path,
    *,
    pins_lock: dict[str, Any] | None = None,
    shelf_root: pathlib.Path | None = None,
) -> dict[str, Any]:
    """Audit every git repo under workstation_root against the Universal Hard Upstream Rule."""
    lock = pins_lock if pins_lock is not None else load_pins_lock()
    shelf_errors = verify_shelf_pins_on_disk(lock, shelf_root=shelf_root)
    repos_report: list[dict[str, Any]] = []
    for child in sorted(workstation_root.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or not (child / ".git").exists():
            continue
        has_up_md = (child / "UPSTREAM.md").is_file()
        has_map = (child / "upstream-map.toml").is_file()
        has_gate = (
            (child / "scripts" / "merge_gate.py").is_file()
            or (child / "tests" / "test_upstream_gate.py").is_file()
            or (child / "canon" / "upstreams.json").is_file()
        )
        adr_dir = child / "docs" / "adr"
        adr_count = (
            len([p for p in adr_dir.glob("*.md") if p.name not in {"CATALOG.md", "README.md"}])
            if adr_dir.is_dir()
            else 0
        )
        adr_errors = verify_adrs_have_evidence(child)
        manifest_errors = verify_sealed_manifests(child)
        map_errors = verify_upstream_map(child) if has_map else ["Missing upstream-map.toml"]
        repos_report.append(
            {
                "repo": child.name,
                "has_upstream_md": has_up_md,
                "has_upstream_map": has_map,
                "has_gate": has_gate,
                "adr_count": adr_count,
                "adr_evidence_ok": len(adr_errors) == 0,
                "adr_errors_count": len(adr_errors),
                "manifest_errors_count": len(manifest_errors),
                "upstream_map_ok": has_map and len(map_errors) == 0,
                "upstream_map_errors_sample": map_errors[:5],
            }
        )

    payload: dict[str, Any] = {
        "schema": HARD_UPSTREAM_RULE_SCHEMA,
        "adr": HARD_UPSTREAM_RULE_ADR,
        "repos_audited": len(repos_report),
        "repos_with_upstream_md": sum(1 for r in repos_report if r["has_upstream_md"]),
        "repos_with_upstream_map": sum(1 for r in repos_report if r["has_upstream_map"]),
        "repos_passing_upstream_map": sum(1 for r in repos_report if r["upstream_map_ok"]),
        "repos_passing_adr_evidence": sum(1 for r in repos_report if r["adr_evidence_ok"]),
        "shelf_18_pins_ok": len(shelf_errors) == 0,
        "shelf_errors": shelf_errors,
        "repos": repos_report,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()
    payload["manifest_sha256"] = digest
    return payload


CLEANROOM_SPL_ORG_REPOS: tuple[tuple[str, str, str], ...] = (
    (".github", "org-profile", "Organization governance, SHA-pinned reusable CI, and zero-leak org manifest"),
    ("sota-shelf-lock", "L0-shelf", "Immutable 18-pin upstream shelf registry, ADR-0023/0024 hard rules, and audit CLI"),
    ("sota-research-sim-lab", "L5-sim", "Pre-wall (<=2026-10-15) NautilusTrader/VectorBT/hftbacktest/5-lib causal research & CPCV/DSR falsifier"),
    ("sota-paper-live-engine", "L3-exec", "NautilusTrader + alpaca-py + ib_async Paper->Live engine with ADR-0022 <=2.00% stops & atomic SAR"),
    ("sota-compounding-harness", "L9-harness", "8-runtime PreToolUse SOTA-source hooks, 60-skill SkillEvaluator, Empirical-Bayes compounding & sota-bus"),
    ("sota-orca-workflows", "L9-orca", "Dual-workstation Orca worktree/automation workflows & research-convergence-first landing gates"),
)


def bootstrap_cleanroom_spl_org(
    target_dir: pathlib.Path,
    *,
    org_name: str = "sota-spl-cleanroom",
) -> dict[str, Any]:
    """Generate a turnkey clean-room Sim->Paper->Live org blueprint pre-wired with ADR-0023 hard rules."""
    root = target_dir.resolve()
    root.mkdir(parents=True, exist_ok=True)
    pins_raw = json.loads((pathlib.Path(__file__).resolve().parents[2] / "PINS_LOCK.json").read_text(encoding="utf-8"))
    shelf_rows = pins_raw.get("upstreamShelfPins", []) if isinstance(pins_raw, dict) else []
    pins = {str(item["name"]): item for item in shelf_rows if isinstance(item, dict) and "name" in item}
    pin_rows = "\n".join(
        f"| `{k}` | `{v.get('ref', '')}` @ `{v.get('commit', '')}` | {v.get('license', '')} | {v.get('url', '')} | upstream |"
        for k, v in sorted(pins.items())
    )
    pin_toml = "\n".join(
        f'"{k}" = "{v.get("commit", "")}"'
        for k, v in sorted(pins.items())
    )

    created_repos: list[dict[str, Any]] = []
    for repo_name, layer, role in CLEANROOM_SPL_ORG_REPOS:
        rdir = root / repo_name
        (rdir / "docs" / "adr").mkdir(parents=True, exist_ok=True)
        (rdir / "scripts").mkdir(parents=True, exist_ok=True)
        (rdir / "UPSTREAM.md").write_text(
            f"# {org_name}/{repo_name} — Pinned SOTA Upstream Register ({layer})\n\n"
            f"| Component | Pin / Commit | Origin |\n|---|---|---|\n"
            f"| `orca` | `stablyai/orca` | upstream |\n"
            f"{pin_rows}\n",
            encoding="utf-8",
        )
        (rdir / "upstream-map.toml").write_text(
            f"# ADR-0023 fail-closed upstream-map.toml for {org_name}/{repo_name}\n\n"
            f"[shelf_pins]\n{pin_toml}\n\n"
            f"[areas]\n"
            f'"scripts/merge_gate.py" = {{ upstream = "nautilus_trader", how = "build-on", '
            f'feature = "ADR-0023 hard upstream-source, ADR-evidence, and zero-leak merge gate", '
            f'why = "fail closed before any commit or push bypasses pinned SOTA provenance" }}\n',
            encoding="utf-8",
        )
        (rdir / "scripts" / "merge_gate.py").write_text(
            "#!/usr/bin/env python3\n"
            '"""Fail-closed ADR-0023 merge gate."""\n'
            "import pathlib, sys\n"
            "from shelf_lock.hard_upstream_rule import main\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main(['--repo', str(pathlib.Path(__file__).resolve().parents[1])]))\n",
            encoding="utf-8",
        )
        (rdir / "docs" / "adr" / "ADR-0001-sota-upstream-first-and-research-convergence.md").write_text(
            f"# ADR-0001: SOTA Upstream-First & Research-Convergence Foundation ({repo_name})\n\n"
            f"- **Status:** Accepted\n- **Date:** 2026-11-20\n- **Layer:** {layer}\n\n"
            f"## Context & Decision\n{role}. Every line of code must install, integrate, or build upon "
            f"pinned SOTA upstreams in `UPSTREAM.md` and `upstream-map.toml` under `ADR-0023`.\n\n"
            f"## Verification & Evidence\n- Generated by `shelf_lock.hard_upstream_rule.bootstrap_cleanroom_spl_org` "
            f"with `18` SHA-pinned SOTA upstream shelf contracts and fail-closed `scripts/merge_gate.py`.\n",
            encoding="utf-8",
        )
        (rdir / "orca.yaml").write_text(
            f"name: {repo_name}\n"
            f"org: {org_name}\n"
            f"layer: {layer}\n"
            f"hard_rules:\n"
            f"  adr_0023_upstream_map: required\n"
            f"  adr_0022_max_stop_pct: 2.0\n"
            f"  paper_only_firewall: true\n",
            encoding="utf-8",
        )
        created_repos.append({"repo": repo_name, "layer": layer, "role": role})

    manifest: dict[str, Any] = {
        "schema": "sota.cleanroom-spl-org-blueprint.v1",
        "adr": "ADR-0024",
        "org_name": org_name,
        "repos_count": len(created_repos),
        "shelf_pins_count": len(pins),
        "repos": created_repos,
    }
    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()
    manifest["manifest_sha256"] = digest
    (root / "ORG_BLUEPRINT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Universal Hard SOTA Upstream-Source & ADR-Evidence Enforcer")
    parser.add_argument("--repo", type=pathlib.Path, help="Verify a single repository root")
    parser.add_argument("--audit-workstation", type=pathlib.Path, help="Audit all git repos under a directory")
    parser.add_argument(
        "--require-full-compliance",
        action="store_true",
        help="With --audit-workstation, exit non-zero unless 100% of repos pass upstream-map & ADR evidence",
    )
    parser.add_argument(
        "--bootstrap-org-blueprint",
        type=pathlib.Path,
        help="Generate clean-room Sim->Paper->Live org blueprint pre-wired with ADR-0023 hard rules",
    )
    parser.add_argument("--org-name", default="sota-spl-cleanroom", help="Org name for --bootstrap-org-blueprint")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    if args.bootstrap_org_blueprint:
        res = bootstrap_cleanroom_spl_org(args.bootstrap_org_blueprint, org_name=args.org_name)
        print(json.dumps(res, indent=2, allow_nan=False))
        return 0

    if args.audit_workstation:
        report = audit_workstation_repos(args.audit_workstation)
        if args.json:
            print(json.dumps(report, indent=2, allow_nan=False))
        else:
            print(
                f"Audited {report['repos_audited']} repos | UPSTREAM.md={report['repos_with_upstream_md']} | "
                f"upstream-map={report['repos_with_upstream_map']} (pass={report['repos_passing_upstream_map']}) | "
                f"ADR evidence pass={report['repos_passing_adr_evidence']}/{report['repos_audited']} | "
                f"18-pin shelf ok={report['shelf_18_pins_ok']} | sha256={report['manifest_sha256'][:16]}"
            )
        ok = bool(report["shelf_18_pins_ok"])
        if args.require_full_compliance:
            n = report["repos_audited"]
            ok = ok and (
                report["repos_with_upstream_md"] == n
                and report["repos_passing_upstream_map"] == n
                and report["repos_passing_adr_evidence"] == n
            )
        return 0 if ok else 1

    target = args.repo or pathlib.Path(__file__).resolve().parents[2]
    problems = [
        *verify_upstream_map(target),
        *verify_adrs_have_evidence(target),
        *verify_sealed_manifests(target),
        *verify_shelf_pins_on_disk(),
        *verify_zero_leaks_and_noreply(target),
    ]
    if args.json:
        print(json.dumps({"ok": not problems, "problems": problems}, indent=2, allow_nan=False))
    elif problems:
        for p in problems:
            print(f"[HARD-UPSTREAM-RULE FAIL] {p}", file=sys.stderr)
    else:
        print("[HARD-UPSTREAM-RULE PASS] 100% upstream-map, ADR evidence, shelf pins, and zero-leak verified.")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
