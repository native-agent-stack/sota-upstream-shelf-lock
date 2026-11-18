"""Owner 413-Starred + Beyond-Starred Frontier SOTA Research Convergence Matrix (`v3.10.0`).

Grounds the `native-agent-stack` 8-Stage Research Convergence Practice and `DF1..DF12`
Symbol Ranking Foundation across:
1. `STARRED_413_RESEARCH_ANCHORS`: Curated anchors across the owner's 413 GitHub stars spanning
   quantitative alpha/backtesting, financial datafeeds, time-series foundation models, agentic
   self-evolution/evaluation, and multi-runtime orchestration.
2. `BEYOND_STARRED_FRONTIER_SOTA_ANCHORS`: Frontier SOTA pillars beyond starred (`microsoft/RD-Agent`
   `RD-Agent(Q)` Co-STEER, `databento/databento-python` bitemporal `ts_event_ns <= ts_recv_ns <=
   decision_ns`, `unit8co/darts` + `Nixtla/statsforecast` conformal baseline hurdles, `stanfordnlp/dspy`
   `MIPROv2`/`GEPA`, and ADIA Lab #19 `MinTRL`/`MDE` + `C(6,2)=15` CPCV + Empirical-Bayes shrinkage).
3. `verify_bitemporal_pit_event`: Fail-closed nanosecond bitemporal latency & lookahead guard.
"""

from __future__ import annotations

import copy
from typing import Any

from shelf_lock.research_workflow import (
    CANONICAL_RESEARCH_FEEDS_V2,
    RESEARCH_FEEDS_SCHEMA_VERSION,
    SIBLING_REPO_AUTHORITY,
)
from shelf_lock.validator import load_pins_lock

CONVERGENCE_MATRIX_SCHEMA_VERSION = "sota-research-convergence-matrix.v3.10"

FINALIZED_12_RANKING_FEED_IDS: tuple[str, ...] = (
    "DF1_alpaca_sip_lit_and_dark_tape",
    "DF2_alpaca_boats_overnight_and_dec6_23x5",
    "DF3_raw_vs_all_split_and_corporate_actions_guard",
    "DF4_xnys_tod_rvol_bucket_normalizer",
    "DF5_sec_edgar_acceptance_datetime_catalyst_and_dilution_shield",
    "DF6_sec_xbrl_point_in_time_public_float",
    "DF7_finra_regsho_cnmsshvol_intraday_t1",
    "DF8_finra_rule4560_settled_short_interest_t8",
    "DF9_vix_majors_regime_and_ibkr_4002_l1_locate",
    "DF10_sip_20session_normal_rate_and_nyse_ucurve_baseline",
    "DF11_bitemporal_nbbo_collar_and_h096_15s_dry_powder_survival",
    "DF12_qlib_cross_sectional_ic_and_real_paper_eb_feedback",
)

STARRED_413_RESEARCH_ANCHORS: dict[str, dict[str, str]] = {
    "microsoft/qlib": {
        "domain": "quant_research",
        "role": "Cross-sectional Rank-IC, ICIR, and rolling PIT factor evaluation",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "openbq-org/OpenBB": {
        "domain": "quant_datafeeds",
        "role": "Normalized macro, fundamental, and equity data-router reference",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "QuantConnect/Lean": {
        "domain": "quant_execution_and_rvol",
        "role": "XNYS time-of-day RelativeDailyVolume baseline and multi-asset fill rules",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "stefan-jansen/machine-learning-for-trading": {
        "domain": "quant_validation",
        "role": "Purged walk-forward feature engineering and deflation hygiene",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "google-research/timesfm": {
        "domain": "time_series_foundation",
        "role": "Zero-shot multi-horizon temporal foundation benchmark",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "shiyu-coder/Kronos": {
        "domain": "financial_foundation_model",
        "role": "OHLCV candlestick tokenization and orderflow regime forecasting",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "AI4Finance-Foundation/FinRL-Trading": {
        "domain": "quant_rl",
        "role": "Portfolio trajectory reward shaping under transaction-cost constraints",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "TauricResearch/TradingAgents": {
        "domain": "multi_agent_finance",
        "role": "Role-separated bull/bear/risk-manager deliberation pattern",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "virattt/dexter": {
        "domain": "financial_research_agent",
        "role": "Autonomous SEC XBRL statement decomposition and validation",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "alphaXiv/OpenResearch": {
        "domain": "scientific_discovery",
        "role": "Primary-literature grounding and reproducible citation verification",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "K-Dense-AI/scientific-agent-skills": {
        "domain": "scientific_skills",
        "role": "Vendored domain-rigorous statistical, EDA, and statsmodels workflows",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "Orchestra-Research/AI-Research-SKILLs": {
        "domain": "research_skills",
        "role": "Pre-registered hypothesis discipline and reproducible ML evals",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "Imbad0202/academic-research-skills": {
        "domain": "research_rigor",
        "role": "Literature synthesis -> experiment -> adversarial falsification pipeline",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "karpathy/autoresearch": {
        "domain": "autonomous_loop",
        "role": "Pre-registered Modify -> Verify -> Keep/Discard fixed-budget loop",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "wanshuiyin/Auto-claude-code-research-in-sleep": {
        "domain": "cross_model_aris",
        "role": "ARIS cross-vendor nocturnal verification and critique",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "microsoft/SkillOpt": {
        "domain": "skill_optimization",
        "role": "Text-space optimization turning execution friction into durable skills",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "NousResearch/hermes-agent-self-evolution": {
        "domain": "evolutionary_skills",
        "role": "GEPA reflective evolutionary prompt and skill compilation",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "NVIDIA/SkillEvaluator": {
        "domain": "skill_evaluation",
        "role": "Multi-tier semantic-overlap and quality-gate evaluation for skills",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "parallel-web/parallel-search-evals": {
        "domain": "search_evals",
        "role": "Empirical recall and factuality benchmark for research retrieval",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "elementalsouls/Claude-BugHunter": {
        "domain": "red_team_audit",
        "role": "External red-team bug-hunting and invariant-breakage checks",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "trailofbits/skills": {
        "domain": "security_and_math",
        "role": "Dimensional unit invariants, IEEE-754 safety, and property testing",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "cloudflare/security-audit-skill": {
        "domain": "security_audit",
        "role": "Two-pass self-refuting vulnerability confirmation without false positives",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "alibaba/open-code-review": {
        "domain": "code_review",
        "role": "Deterministic static checks paired with stateful multi-file review",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "backnotprop/plannotator": {
        "domain": "plan_governance",
        "role": "Interactive specification review and human-in-the-loop checkpoints",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "OthmanAdi/planning-with-files": {
        "domain": "durable_state",
        "role": "Crash-proof disk-backed plan/findings/progress state across compaction",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "DeusData/codebase-memory-mcp": {
        "domain": "code_graph_mcp",
        "role": "Persistent 66-language symbol and call-chain impact graph over MCP",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "xerj-org/xerj": {
        "domain": "agent_search_mcp",
        "role": "Fast Rust codebase/doc/log index for sub-millisecond retrieval",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "MinishLab/semble": {
        "domain": "token_efficient_search",
        "role": "Token-frugal symbol-level discovery before file reads",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "headroomlabs-ai/headroom": {
        "domain": "context_compression",
        "role": "Tool-output compression before LLM context ingestion",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "rtk-ai/rtk": {
        "domain": "cli_compression",
        "role": "CLI output token reduction proxy for heavy test/lint runs",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "stablyai/orca": {
        "domain": "worktree_orchestrator",
        "role": "Isolated git worktree fleet, automations, and cross-host agent DAGs",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "Yeachan-Heo/oh-my-claudecode": {
        "domain": "claude_orchestration",
        "role": "OMC runtime v2 multi-session coordination and stop callbacks",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "Yeachan-Heo/oh-my-codex": {
        "domain": "codex_orchestration",
        "role": "OMX mission and exec non-interactive cross-vendor review",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "code-yeongyu/oh-my-openagent": {
        "domain": "openagent_orchestration",
        "role": "Non-GPT Hephaestus structured graph refactoring",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "can1357/oh-my-pi": {
        "domain": "pi_orchestration",
        "role": "Role-selected thinking-effort workers (`@worker`)",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "aaif-goose/goose": {
        "domain": "aaif_agent",
        "role": "AAIF MCP-native autonomous CLI recipe execution",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "deepseek-ai/deepseek-harness": {
        "domain": "dsh_harness",
        "role": "10-layer plugin harness and pre-wall batch probe verification",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "aannoo/hcom": {
        "domain": "terminal_bus",
        "role": "Cross-terminal live wakeup and agent messaging spine",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "gastownhall/beads": {
        "domain": "task_dag_memory",
        "role": "Git-backed dependency task graph (`bd`) across waves",
        "authority": SIBLING_REPO_AUTHORITY,
    },
}

BEYOND_STARRED_FRONTIER_SOTA_ANCHORS: dict[str, dict[str, str]] = {
    "microsoft/RD-Agent": {
        "pillar": "RD-Agent(Q) Co-STEER",
        "role": "Alternating Factor-Hypothesis <-> Model-Hypothesis evolutionary research loop",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "databento/databento-python": {
        "pillar": "Bitemporal Nanosecond PIT",
        "role": "Strict ts_event_ns <= ts_recv_ns <= decision_ns latency and clock-skew lookahead guard",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "unit8co/darts+Nixtla/statsforecast": {
        "pillar": "Conformal Time-Series & Zero-Leakage Baselines",
        "role": "Calibrated prediction intervals and fast seasonal/naive benchmark hurdles",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "stanfordnlp/dspy": {
        "pillar": "MIPROv2 / GEPA Prompt-Program Compilation",
        "role": "Metric-driven optimizer paired with Microsoft SkillOpt for deterministic skill tuning",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "adia-lab-19+mlfinlab": {
        "pillar": "ADIA Lab #19 MinTRL/MDE + Triple-Barrier + CPCV + Empirical Bayes",
        "role": "Finite-sample power gate, C(6,2)=15 purged CV, DSR >= 0.95, and kappa=40 shrinkage",
        "authority": SIBLING_REPO_AUTHORITY,
    },
}


def verify_bitemporal_pit_event(
    ts_event_ns: int,
    ts_recv_ns: int,
    decision_ns: int,
) -> tuple[bool, list[str]]:
    """Verify strict bitemporal ordering `0 < ts_event_ns <= ts_recv_ns <= decision_ns`."""
    reasons: list[str] = []
    values = (("ts_event_ns", ts_event_ns), ("ts_recv_ns", ts_recv_ns), ("decision_ns", decision_ns))
    for label, val in values:
        if isinstance(val, bool) or not isinstance(val, int):
            reasons.append(f"BITEMPORAL_INVALID_TYPE:{label}={val!r}")
        elif val <= 0:
            reasons.append(f"BITEMPORAL_NON_POSITIVE:{label}={val}")
    if reasons:
        return False, reasons
    if ts_event_ns > ts_recv_ns:
        reasons.append(f"BITEMPORAL_CLOCK_SKEW_LOOKAHEAD:ts_event_ns({ts_event_ns})>ts_recv_ns({ts_recv_ns})")
    if ts_recv_ns > decision_ns:
        reasons.append(f"BITEMPORAL_DECISION_LOOKAHEAD:ts_recv_ns({ts_recv_ns})>decision_ns({decision_ns})")
    return (len(reasons) == 0), reasons


def build_sota_research_convergence_matrix_manifest() -> dict[str, Any]:
    """Emit the unified v3.10.0 18-Pin + 413-Starred + Beyond-Starred + DF1..DF12 Convergence Matrix."""
    pins_doc = load_pins_lock()
    pins = pins_doc.get("upstreamShelfPins", [])
    return {
        "schema_version": CONVERGENCE_MATRIX_SCHEMA_VERSION,
        "ecosystem_semver": "3.10.0",
        "research_feeds_schema_v2": RESEARCH_FEEDS_SCHEMA_VERSION,
        "v2_feed_count": len(CANONICAL_RESEARCH_FEEDS_V2),
        "finalized_symbol_ranking_feeds_count": len(FINALIZED_12_RANKING_FEED_IDS),
        "finalized_symbol_ranking_feed_ids": list(FINALIZED_12_RANKING_FEED_IDS),
        "immutable_core_pins_count": len(pins),
        "starred_413_anchors_count": len(STARRED_413_RESEARCH_ANCHORS),
        "beyond_starred_frontier_anchors_count": len(BEYOND_STARRED_FRONTIER_SOTA_ANCHORS),
        "sibling_repo_authority": SIBLING_REPO_AUTHORITY,
        "starred_413_anchors": copy.deepcopy(STARRED_413_RESEARCH_ANCHORS),
        "beyond_starred_frontier_anchors": copy.deepcopy(BEYOND_STARRED_FRONTIER_SOTA_ANCHORS),
    }
