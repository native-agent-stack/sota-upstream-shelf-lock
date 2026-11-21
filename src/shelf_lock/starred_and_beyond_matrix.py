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
    # --- ADR-0026: Live-Verified 2026-11-20 Active, Non-Archived, SPDX-Licensed LLM-Native Quant Frontier ---
    "nautechsystems/nautilus_agents": {
        "pillar": "Rust-Native NautilusTrader Agents SDK",
        "role": "Official Rust types, traits & agent engine on NautilusTrader (zero order-path leak verified)",
        "head_sha": "380ae38f353355cdd4a9eb58a51baa8bb01e583d",
        "spdx_license": "LGPL-3.0",
        "layer_target": "L2/L5/L8",
        "order_path_policy": "NO_ORDER_PATH_VERIFIED",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "anthropics/financial-services": {
        "pillar": "Official Financial Services Agent Plugins",
        "role": "Anthropic financial-analysis, Earnings Reviewer, Market Researcher & MCP connectors (41.4k stars)",
        "head_sha": "3e32c2287dcb637c184c01cc0ad82d6af7e9bb0f",
        "spdx_license": "Apache-2.0",
        "layer_target": "L3/L8",
        "order_path_policy": "NO_ORDER_PATH_VERIFIED",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "waylonli/FINSABER": {
        "pillar": "KDD 2026 Leakage-Free & Token-Cost Backtest Harness",
        "role": "Kills LLM pre-training cutoff leakage; enforces next_open/slippage/liquidity & inference cost accounting",
        "head_sha": "e72c26206d08de2ffeab736b96878109f144040f",
        "spdx_license": "Apache-2.0",
        "layer_target": "L4",
        "order_path_policy": "BACKTEST_EVAL_ONLY_BLOCK_VENDORED_BROKER",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "microsoft/MarS": {
        "pillar": "ICLR 2025 Large Market Model (Order-Level Generative LOB)",
        "role": "Order-level generative foundation model for interactive market-impact & counterfactual LOB simulation",
        "head_sha": "f04dd87a4d56342a6a2fc271cdb158fbacd83674",
        "spdx_license": "MIT",
        "layer_target": "L2/L12/L13",
        "order_path_policy": "SIMULATION_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "peernagy/LOBS5": {
        "pillar": "State-Space Generative LOB Simulator & LOB-Bench Parity",
        "role": "Autoregressive S5 model + Jax-LOB verifying price-impact curves & stylized microstructure fidelity",
        "head_sha": "aa36029e9d348a017d00efc37c6b6dda89fab150",
        "spdx_license": "MIT",
        "layer_target": "L2/L12",
        "order_path_policy": "SIMULATION_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "AI4Finance-Foundation/FinRobot": {
        "pillar": "Deterministic Tool-Backed Financial Agent Platform",
        "role": "Models reason, software computes, systems verify — modular PydanticAI/FastAPI equity & quant workflows",
        "head_sha": "63e1884a42ea7b729551a5424b4bd6a65af636e0",
        "spdx_license": "Apache-2.0",
        "layer_target": "L3/L6",
        "order_path_policy": "RESEARCH_TOOL_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "HKUDS/Vibe-Trading": {
        "pillar": "Skill-Native Personal Trading Research Harness",
        "role": "Natural-language-to-strategy skill presets & backtest workflows (38.6k stars; sandboxed reference only)",
        "head_sha": "25c89a0aa21d72d9eb2303c14f6c1524dd8aed1e",
        "spdx_license": "MIT",
        "layer_target": "L3/L8",
        "order_path_policy": "SANDBOX_RESEARCH_ONLY_NO_BROKER_KEYS",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "aliyun/qwen-dianjin": {
        "pillar": "Local RTX 4090 GRPO Financial Reasoning & Process Reward Model",
        "role": "DianJin-R1-7B/32B + Fin-PRM + OCR-R1 for zero-cost local SEC/earnings reasoning & step verification",
        "head_sha": "a626b083c1c3ff776a88c3c684ec0e186e622c62",
        "spdx_license": "MIT",
        "layer_target": "L1/L3/L7",
        "order_path_policy": "NO_ORDER_PATH_VERIFIED",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "The-FinAI/Fino1": {
        "pillar": "Open-Weight Financial Chain-of-Thought RL Reasoner",
        "role": "Fino1-14B SFT+GRPO FinCoT optimized for FinQA, DocMath-Eval & XBRL-Math numerical verification",
        "head_sha": "f2b9e9931778d806ff9dd0fbb299b0ce1a2c3398",
        "spdx_license": "MIT",
        "layer_target": "L3/L4/L7",
        "order_path_policy": "NO_ORDER_PATH_VERIFIED",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "The-FinAI/FinBen": {
        "pillar": "Holistic Financial LLM Evaluation Harness",
        "role": "lm-evaluation-harness benchmark grading financial LLMs across quantitative reasoning, filings & risk",
        "head_sha": "74ea6b8f8fcdee51f49281634982a8f29da52e7e",
        "spdx_license": "MIT",
        "layer_target": "L4/L15",
        "order_path_policy": "EVAL_BENCHMARK_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "PriorLabs/TabPFN": {
        "pillar": "Tabular In-Context Foundation Model",
        "role": "Zero-tuning tabular foundation model for small-sample multi-factor cross-sectional scoring on RTX 4090",
        "head_sha": "e1a3550654df04bf8428fd1a2c4e8ebe2d805796",
        "spdx_license": "Apache-2.0",
        "layer_target": "L3/L7",
        "order_path_policy": "MODEL_INFERENCE_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "amazon-science/chronos-forecasting": {
        "pillar": "Chronos-2 Multivariate & Macro-Covariate TSFM",
        "role": "120M encoder T5 with group-attention multivariate & exogenous macro-covariate forecasting",
        "head_sha": "1224fafa91e1ecd6674f5204066b159e40b5e4a1",
        "spdx_license": "Apache-2.0",
        "layer_target": "L3/L7/L11",
        "order_path_policy": "MODEL_INFERENCE_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "SalesforceAIResearch/uni2ts": {
        "pillar": "MOIRAI-2 Multi-Quantile Risk Foundation Model",
        "role": "Fast decoder-only universal TSFM with pinball/quantile loss mapping directly to VaR & Expected Shortfall",
        "head_sha": "cfd46d4510ed8896f263116f32928eede05b0a75",
        "spdx_license": "Apache-2.0",
        "layer_target": "L7/L11",
        "order_path_policy": "MODEL_INFERENCE_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "online-ml/river": {
        "pillar": "Streaming CUSUM / ADWIN / Page-Hinkley Alpha-Decay Gate",
        "role": "Incremental online concept-drift & CUSUM sequential change-point detection for live expectancy kill-switches",
        "head_sha": "5ea245400645aba5239e4fcb19b59b756d2e9e53",
        "spdx_license": "BSD-3-Clause",
        "layer_target": "L14",
        "order_path_policy": "DRIFT_MONITOR_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "scikit-learn-contrib/MAPIE": {
        "pillar": "Distribution-Free Conformal Risk & Prediction Intervals",
        "role": "Adaptive conformal prediction bands for dynamic VaR, stop-loss bounds & out-of-sample risk guarantees",
        "head_sha": "e4c4f5f7daeaa7c8b09323852ad1997e506891a2",
        "spdx_license": "BSD-3-Clause",
        "layer_target": "L11",
        "order_path_policy": "RISK_QUANTIFICATION_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "py-why/dowhy": {
        "pillar": "Causal Inference & Refutation for Execution & Alpha Attribution",
        "role": "Structural causal modeling, refutation & Double-ML execution/routing impact attribution (with py-why/EconML)",
        "head_sha": "45de9a90623bae166e32790a6bb5a77827ef91cd",
        "spdx_license": "MIT",
        "layer_target": "L4/L12",
        "order_path_policy": "CAUSAL_ATTRIBUTION_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "massive-com/mcp_massive": {
        "pillar": "Official Massive.com (formerly Polygon.io) Market & Options MCP",
        "role": "Read-only real-time/historical equities, options, futures & crypto MCP with in-memory SQLite analytics",
        "head_sha": "1e161a8c50b69bd467b092e0721e30908ab94eb6",
        "spdx_license": "MIT",
        "layer_target": "L1/L13",
        "order_path_policy": "NO_ORDER_PATH_VERIFIED",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "BrainDAO/mcp-polymarket": {
        "pillar": "Live Event-Contract Implied-Probability MCP (Read-Only)",
        "role": "Gamma order-book macro/Fed/CPI/earnings implied-probability signal feed (strictly zero private key)",
        "head_sha": "5360bef548afded0770e27b296ef467e78894f2f",
        "spdx_license": "MIT",
        "layer_target": "L1/L13",
        "order_path_policy": "READ_ONLY_ZERO_PRIVATE_KEY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
    "FreedomIntelligence/TwinMarket": {
        "pillar": "NeurIPS/ICLR 2025 Best-Paper BDI Market Contagion Simulator",
        "role": "Multi-agent Belief-Desire-Intention socio-economic simulator for herding, bubbles & flash-crash stress tests",
        "head_sha": "de5f2446fcba0d0aba533a6adaede034160e29b4",
        "spdx_license": "MIT",
        "layer_target": "L11/L13",
        "order_path_policy": "SIMULATION_ONLY",
        "authority": SIBLING_REPO_AUTHORITY,
    },
}

LICENSE_AND_ARCHIVE_QUARANTINE_WATCHLIST: dict[str, dict[str, str]] = {
    "QuantaAlpha/QuantaAlpha": {
        "status": "UNLICENSED_RESEARCH_REFERENCE_ONLY",
        "spdx_license": "NONE",
        "head_sha": "b7ceb27b1001261d7a95b209a963664ae1f8ab23",
        "reason": "High-value evolutionary crowding-pruned alpha mining paper/design, but GitHub repo has no LICENSE — never vendor code.",
    },
    "SUFE-AIFLM-Lab/Fin-R1": {
        "status": "UNLICENSED_RESEARCH_REFERENCE_ONLY",
        "spdx_license": "NONE",
        "head_sha": "06ead1e61ff77cad71dc409198b1a2575d748ecd",
        "reason": "No LICENSE on GitHub & last pushed 2025-03-27; use MIT-licensed aliyun/qwen-dianjin or The-FinAI/Fino1 instead.",
    },
    "FinStep-AI/Alpha-R1": {
        "status": "UNLICENSED_RESEARCH_REFERENCE_ONLY",
        "spdx_license": "NONE",
        "head_sha": "5a55d35c2efb9157b5d58f869d2c8c1afb511768",
        "reason": "No LICENSE on GitHub — GRPO return-rewarded alpha-screening methodology reference only.",
    },
    "horizon-llm/AlphaQuanter": {
        "status": "UNLICENSED_RESEARCH_REFERENCE_ONLY",
        "spdx_license": "NONE",
        "head_sha": "fac423cb1b45a3d0593e88a0f9805c338d7e0fea",
        "reason": "ACL 2026 single-agent tool-orchestrated RL architecture reference only; GitHub repo has no LICENSE.",
    },
    "patronus-ai/financebench": {
        "status": "UNLICENSED_EVAL_REFERENCE_ONLY",
        "spdx_license": "NONE",
        "head_sha": "cc39aeb4afdf33909ee1412188bf89035950c2eb",
        "reason": "No LICENSE on GitHub; prefer MIT-licensed The-FinAI/FinBen for automated eval harnesses.",
    },
    "hansbuehler/deephedging": {
        "status": "GPL3_STRONG_COPYLEFT_ISOLATED",
        "spdx_license": "GPL-3.0",
        "head_sha": "fe53fd9a7e402d4ba18bd5b9ec704e0361554f7c",
        "reason": "GPL-3.0 strong copyleft — research methodology reference for friction-aware deep hedging, never linked into permissive core.",
    },
    "OpenBB-finance/agents-for-openbb": {
        "status": "ARCHIVED_SUPERSEDED",
        "spdx_license": "MIT",
        "head_sha": "aa1073d2b098ae6cf597dabf0635822aa808dd81",
        "reason": "Archived 2026-07-01; superseded by official openbq-org/OpenBB & openbq-org/finos-workspace.",
    },
    "Polymarket/agents": {
        "status": "ARCHIVED_SUPERSEDED",
        "spdx_license": "MIT",
        "head_sha": "081f2b5594c37edeb9d3780a778c084d5b6f2743",
        "reason": "Archived 2024-11-05; superseded by active MIT BrainDAO/mcp-polymarket (read-only zero private key).",
    },
    "jpmorganchase/abides-jpmc-public": {
        "status": "ARCHIVED_REFERENCE_ONLY",
        "spdx_license": "NOASSERTION",
        "head_sha": "f9cbe51342b7dedd9587e4e069040d68a5c6477f",
        "reason": "Archived 2024-07-22; superseded by active MIT microsoft/MarS & peernagy/LOBS5.",
    },
    "hummingbot/mcp": {
        "status": "ARCHIVED_SKIP",
        "spdx_license": "Apache-2.0",
        "head_sha": "836f9351d48e5c293eaad3ffa16b55fa7bad1a98",
        "reason": "Archived 2026-03-23; skipped under active-maintenance policy.",
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
