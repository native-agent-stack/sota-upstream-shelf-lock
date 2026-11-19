# Upstream SOTA Frameworks & 18-Pin Quantitative Shelf Lineage (`v3.10.9`)

Repository: `https://github.com/native-agent-stack/sota-upstream-shelf-lock` · Plane & Lane: `H2_UPSTREAM_40SHA_SHELF_LOCK` · DataFeed Contract: `sota-ranking-datafeeds.v3.10` (`DF1..DF12` + `DF1..DF9` compat) · Canonical Skills: `60` · Canonical Workflows: `21` · Starred Convergence: `415` starred + `8` beyond-starred (`STARRED_CONVERGENCE_CATALOG.json`) · RTX 4090 CUDA Sidecar: `:8794` (`ADR-0036`) · Doctor: `18/18`.

## 1. Multi-Model Runtime Workers & Active Orchestration Stack (`v3.10.9`, Zero Stale / Zero Kimi; `goose` & `grok` Retired)

- **Cross-Machine Supervisor (`stablyai/orca` `v1.4.263` live / `v1.4.264` available):** Symmetric `:6770` `Mac M5 Max (100.93.211.101) <-> Noesis (100.110.115.22)` E2EE mesh, `sota-orca-lane-hub.v2` `9/9` 3-surface folder hubs (`Win32`, `Noesis-Carbon (WSL)`, `Mac M5 Max`), `10/10` canonical lane leads, `17/17` dual-machine SOTA automations (`15` canonical standing + `2` multihour), and post-cutover stationary-primary firewall (`singleActiveBrokerHostOnly = true`).
- **Sovereign Lead Orchestrator (`anthropics/claude-code` `v2.1.328` live + `Yeachan-Heo/oh-my-claudecode` `v5.8.6` compiled dist; upstream release `v5.8.4`):** `claude-fable-5-2` (`xhigh`, `OMC_RUNTIME_V2=1`, `oneModelPerConversation=true`) + `claude-opus-5-5` (`high`) + `claude-sonnet-5-5` (`high`, `OMC_MODEL_LOW=claude-sonnet-5-5`).
- **Cross-Family Adversarial Critic (`openai/codex` `0.169.0` pinned / `rust-v0.170.0` evaluated + `Yeachan-Heo/oh-my-codex` `v0.22.10` pinned / `v0.22.11` evaluated + `max-sixty/worktrunk` `0.81.0`):** `gpt-6.2-astra` (`xhigh` critic) & `gpt-6.2-sol` (`high` implementation/pytest) in isolated git worktrees.
- **8-Slot Lifecycle & Peer Spine (`ComposioHQ/agent-orchestrator` + `aannoo/hcom` + `steveyegge/beads` + `omniroute`):** 8-slot cross-vendor `AO` convergence, SQLite WAL `peer_bus.db`, `hcom` PTY push & `bd` DAG tracking.
- **Schema-Typed Python DAGs (`agy` `1.5.12` live + `google-antigravity/antigravity-sdk-python`):** `21` canonical `run_workflow` Python DAGs (`gemini-4-neon-xhigh` / `gemini-4-neon-high` flagship alongside `gemini-4-carbon-high` 1M context, `gemini-4-hydrogen-xhigh`, and `gemini-4-argon-high`) + Native Swarm `workspace:share`.
- **Non-GPT Polyglot Graph Runtime (`code-yeongyu/oh-my-openagent` `v5.1.75` pinned / `v5.1.79` evaluated):** `claude-sonnet-5-5` / `deepseek-v4.1-flash` `Hephaestus` (`forbids_gpt_on_hephaestus=true`).
- **Role-Selected Thinking Workers (`can1357/oh-my-pi` `v18.22.0` pinned / `v19.0.0` evaluated):** `gpt-6.2-sol` (`--thinking=high`) explicit workers (`block/goose` and `grok` retired from the active required fleet).
- **Open-Weights Pre-Wall Evaluator (`native-agent-stack/dsh-sota-harness` `v0.2.2-rc.2`):** `deepseek-v4.1-flash` (official `dsh` slug `deepseek-flash`, 1M context) 10-layer offline probes & `<= 2026-10-15` pre-wall batch evaluator.

## 2. 18 Immutable `40`-Hex Quantitative & Execution Upstream Shelf Pins (`DF1..DF12`)

- `alpacahq/alpaca-py` @ `c42add7c0a7026e2ead3ed64e76f4def2b99fda4` (`v0.45.0` — `DF1` SIP, `DF2` BOATS / Dec-6 `23/5`)
- `alpacahq/alpaca-mcp-server` @ `63cc4278d87b31f3ed4efcfaa55624095c6d7be8` (`v2.4.1`)
- `nautechsystems/nautilus_trader` @ `da6b57aefdd62b44f675e434ffcfefca7f4025dd` (`v2.0.0rc9` — `Stage 1` / `:4002` simulation)
- `gmatrunich/nautilus-alpaca` @ `59685d56631b981018a189b5ced1a7000a50bfbd` (`main`)
- `pola-rs/polars` @ `7f902bd3ffd27ff82d14278a09a295ff2f7aed92` (`py-2.1.0` — `DF3` `RAW`-vs-`ALL`, `DF10` 20-session normal-rate lake)
- `duckdb/duckdb` @ `d54cbbe3df17e8e5ce68312f483b4155836112aa` (`v2.0.0` — `DF7` FINRA RegSHO `T-1`)
- `dgunning/edgartools` @ `574c2bd15f6c629bceef03b6550ea8ac8abf3473` (`v6.2.0` — `DF5` SEC `acceptanceDateTime`, `DF6` XBRL public float)
- `ml4t/diagnostic` @ `19e76072e64a18c9ba56130e4a7bcc0bc871f57e` (`v0.2.0` — `DSR` / `PBO` / ADIA Lab #19 `MinTRL`)
- `skfolio/skfolio` @ `90e3fb907fab39d244d899f3caf4e9676889309c` (`v1.12.7` — `CombinatorialPurgedCV`)
- `nkaz001/hftbacktest` @ `5f3ec40b2afb764e0fea112f941ed85523ef4e88` (`main` — `RiskAdverseQueueModel` `100x` round-lot queue, `DF11`)
- `ib-api-reloaded/ib_async` @ `ab629f34c1823ea4c1542f32f07377208a86bdfd` (`v2.1.0` — `DF9` IBKR `:4002` Paper `L1`)
- `finos/perspective` @ `0264ec13cd28ef4a2a136c8ef021c3c112bc8990` (`v5.9.2`)
- `tradingview/lightweight-charts` @ `c29c51e1e5bc61981da5832c97797cb8283d120f` (`master`)
- `ranaroussi/quantstats` @ `d1a214fb906e76f974f45cdccf923b601c67a756` (`main` — `DF12` tear-sheet)
- `polakowo/vectorbt` @ `a52a984b631624bb9daf41cb19f532fe559cf0ef` (`v1.2.0`)
- `unionai-oss/pandera` @ `02b375ab43f39f8c5c5108695c1791fa04f99a26` (`v0.35.0`)
- `gerrymanoim/exchange_calendars` @ `dbe38b1f6887434bbdd1a7d2df6ff8f1742a048a` (`4.13.2` — `DF4` `XNYS` `RVOL_tod`, `DF8` Rule 4560 `T+8`)
- `statsmodels/statsmodels` @ `278ff9950636cdd4939b4055e339a8e681d79cab` (`v0.15.0` — date-clustered HAC SEs)

## 3. Live Upstream Audit Ledger (`2026-11-18`)

Per `ADR-0001` and `ADR-0013`, the `18` locked `40`-char commit SHAs in `PINS_LOCK.json` remain frozen in lockstep with `~/Documents/upstream` (`18/18` verified exact SHA parity) and cross-repo `uv.lock` / `upstream-map.toml` files until an explicit multi-repo regression cutover:

- **Current (`10/18`):** `alpaca-py` (`v0.45.0`), `alpaca-mcp-server` (`v2.4.1`), `nautilus_trader` (`v2.0.0rc9`, latest prerelease), `nautilus-alpaca` (`main`), `polars` (`py-2.1.0`), `duckdb` (`v2.0.0`), `hftbacktest` (`main`), `ib_async` (`v2.1.0`), `quantstats` (`main`), `statsmodels` (`v0.15.0`).
- **Evaluated & Held Minor/Patch Candidates (`8/18` — deferred to next scheduled lockfile cutover):**
  - `edgartools` (`v6.2.0` -> `v6.3.0`), `ml4t-diagnostic` (`v0.2.0` -> `v0.2.1`), `skfolio` (`v1.12.7` -> `v1.13.0`), `perspective` (`v5.9.2` -> `v5.9.3`), `lightweight-charts` (`c29c51e1e5` -> `dbd6ae7831`), `vectorbt` (`v1.2.0` -> `v1.2.1`), `pandera` (`v0.35.0` -> `v0.36.0`), `exchange_calendars` (`4.13.2` -> `4.13.3`).
