# ADR-0026: Live-Verified LLM-Native Quant, Microstructure Foundation Models, Causal/Conformal Risk & License-Firewall Landscape (`2026-11-20`)

- **Status:** Accepted
- **Date:** 2026-11-20
- **Evidence Grade:** E4 (`gh api` live 40-char HEAD SHA + SPDX license + archive status verified across `36` repositories on `2026-11-20`; inspect-only shallow source audit in `Z:/sota-cache/llm-native-eval-pass2/` across `8` frontier repos verifying manifests, API keys & order-placement code paths; `pytest`, `ruff`, `ty`, `scripts/architecture_catalog.py --check`, `scripts/merge_gate.py`, `gitleaks 0`)
- **Supersedes / Extends:** Extends `ADR-0013`, `ADR-0015`, `ADR-0020`, `ADR-0021`, `ADR-0022`, `ADR-0023`, and `ADR-0025`

## Context

Between 2025 and late 2026, LLM-native quantitative trading and AI-native financial tooling diverged sharply into two camps:
1. Unverified prompt-only multi-agent wrappers (`FinMem`, `FinCon`, persona demos) that KDD 2026 (`waylonli/FINSABER`) empirically proved suffer from pre-training cutoff leakage ("profit mirage") and collapse out-of-sample once slippage, liquidity caps, and inference token costs are modeled.
2. High-rigor institutional, academic, and official vendor repositories providing Rust-native agent SDKs (`nautechsystems/nautilus_agents`), official financial plugins (`anthropics/financial-services`), leakage-free evaluation harnesses (`waylonli/FINSABER`), generative limit-order-book foundation models (`microsoft/MarS`, `peernagy/LOBS5`), local RTX 4090 GRPO financial reasoners & tabular/time-series foundation models (`aliyun/qwen-dianjin`, `The-FinAI/Fino1`, `PriorLabs/TabPFN`, `amazon-science/chronos-forecasting`, `SalesforceAIResearch/uni2ts`), streaming drift/conformal/causal inference libraries (`online-ml/river`, `scikit-learn-contrib/MAPIE`, `py-why/dowhy`), and read-only market/event MCP servers (`massive-com/mcp_massive`, `BrainDAO/mcp-polymarket`).

Simultaneously, live GitHub API and source inspection exposed critical licensing, archival, and order-path hazards that static web lists miss:
- Popular academic repos (`QuantaAlpha/QuantaAlpha`, `SUFE-AIFLM-Lab/Fin-R1`, `FinStep-AI/Alpha-R1`, `horizon-llm/AlphaQuanter`, `patronus-ai/financebench`) carry **no GitHub license (`NONE`)**, prohibiting code vendoring.
- Legacy repos (`OpenBB-finance/agents-for-openbb`, `Polymarket/agents`, `jpmorganchase/abides-jpmc-public`, `hummingbot/mcp`) are **archived**, with `openbq-org/OpenBB` (`75,607` stars) confirmed as the official active OpenBB continuation and `BrainDAO/mcp-polymarket` (`MIT`) as the active Polymarket MCP.
- `HKUDS/Vibe-Trading`, `BrainDAO/mcp-polymarket`, and vendored `rl_traders/finrl` inside `waylonli/FINSABER` contain broker/exchange order-routing paths requiring strict read-only / zero-broker-key containment under `ADR-0022`.

## Decision

1. **Expand `BEYOND_STARRED_FRONTIER_SOTA_ANCHORS` in `src/shelf_lock/starred_and_beyond_matrix.py`** with `19` live-verified, active, non-archived, SPDX-licensed frontier repositories — each recording its exact 40-char `head_sha` (verified `2026-11-20`), `spdx_license`, `layer_target` (`L1`–`L15`), and explicit `order_path_policy` (`NO_ORDER_PATH_VERIFIED`, `SIMULATION_ONLY`, `BACKTEST_EVAL_ONLY_BLOCK_VENDORED_BROKER`, `READ_ONLY_ZERO_PRIVATE_KEY`, `SANDBOX_RESEARCH_ONLY_NO_BROKER_KEYS`, etc.).
2. **Enforce `LICENSE_AND_ARCHIVE_QUARANTINE_WATCHLIST` Fail-Closed:** Explicitly quarantine all unlicensed (`NONE`), strong-copyleft (`GPL-3.0`), and archived repositories so zero unlicensed or archived code can be vendored into production repositories.
3. **Preserve Immutable Core 18-Pin Shelf Boundary:** Adding Beyond-Starred research anchors updates the research convergence catalog and `ADR-0045`/`ADR-0048` 16-layer manifest without mutating `~/Documents/upstream/` or `PINS_LOCK.json` until an explicit promotion ADR passes full verification.

## Primary GitHub Evidence (`2026-11-20` Live Verified)

- Rust-Native Nautilus Agents SDK: https://github.com/nautechsystems/nautilus_agents (`LGPL-3.0`, `380ae38f353355cdd4a9eb58a51baa8bb01e583d`, zero order-path code verified)
- Anthropic Financial Services Plugins: https://github.com/anthropics/financial-services (`Apache-2.0`, `41,423` stars, `3e32c2287dcb637c184c01cc0ad82d6af7e9bb0f`, zero order-path code verified)
- FINSABER (KDD 2026 Oral): https://github.com/waylonli/FINSABER (`Apache-2.0`, `e72c26206d08de2ffeab736b96878109f144040f`)
- Microsoft MarS (ICLR 2025 LMM): https://github.com/microsoft/MarS (`MIT`, `1,891` stars, `f04dd87a4d56342a6a2fc271cdb158fbacd83674`)
- LOBS5 / LOB-Bench: https://github.com/peernagy/LOBS5 (`MIT`, `aa36029e9d348a017d00efc37c6b6dda89fab150`)
- FinRobot: https://github.com/AI4Finance-Foundation/FinRobot (`Apache-2.0`, `8,457` stars, `63e1884a42ea7b729551a5424b4bd6a65af636e0`)
- HKUDS Vibe-Trading: https://github.com/HKUDS/Vibe-Trading (`MIT`, `38,619` stars, `25c89a0aa21d72d9eb2303c14f6c1524dd8aed1e`, sandbox-only / zero broker keys)
- Alibaba Qwen DianJin (`DianJin-R1` / `Fin-PRM`): https://github.com/aliyun/qwen-dianjin (`MIT`, `645` stars, `a626b083c1c3ff776a88c3c684ec0e186e622c62`, zero order-path code verified)
- The-FinAI Fino1 & FinBen: https://github.com/The-FinAI/Fino1 (`MIT`, `f2b9e9931778d806ff9dd0fbb299b0ce1a2c3398`) & https://github.com/The-FinAI/FinBen (`MIT`, `74ea6b8f8fcdee51f49281634982a8f29da52e7e`)
- PriorLabs TabPFN: https://github.com/PriorLabs/TabPFN (`Apache-2.0`, `8,502` stars, `e1a3550654df04bf8428fd1a2c4e8ebe2d805796`)
- Amazon Chronos-2: https://github.com/amazon-science/chronos-forecasting (`Apache-2.0`, `6,333` stars, `1224fafa91e1ecd6674f5204066b159e40b5e4a1`)
- Salesforce MOIRAI-2 (`uni2ts`): https://github.com/SalesforceAIResearch/uni2ts (`Apache-2.0`, `1,630` stars, `cfd46d4510ed8896f263116f32928eede05b0a75`)
- Online-ML River (CUSUM/ADWIN): https://github.com/online-ml/river (`BSD-3-Clause`, `6,152` stars, `5ea245400645aba5239e4fcb19b59b756d2e9e53`)
- MAPIE Conformal Risk: https://github.com/scikit-learn-contrib/MAPIE (`BSD-3-Clause`, `1,696` stars, `e4c4f5f7daeaa7c8b09323852ad1997e506891a2`)
- PyWhy DoWhy & EconML: https://github.com/py-why/dowhy (`MIT`, `8,410` stars, `45de9a90623bae166e32790a6bb5a77827ef91cd`)
- Massive.com (formerly Polygon.io) MCP: https://github.com/massive-com/mcp_massive (`MIT`, `405` stars, `1e161a8c50b69bd467b092e0721e30908ab94eb6`, zero order-path code verified)
- BrainDAO Polymarket MCP: https://github.com/BrainDAO/mcp-polymarket (`MIT`, `5360bef548afded0770e27b296ef467e78894f2f`, strictly read-only / zero private key)
- FreedomIntelligence TwinMarket (NeurIPS/ICLR 2025 Best Paper): https://github.com/FreedomIntelligence/TwinMarket (`MIT`, `de5f2446fcba0d0aba533a6adaede034160e29b4`)
- Official OpenBB Continuation: https://github.com/openbq-org/OpenBB (`75,607` stars, `f0f1852b96dd3fc4d5868f8863cbe053ff49c6cd`)

## Consequences

- Every frontier LLM-native quant, microstructure, causal, conformal, and MCP anchor in the ecosystem now has live-verified 40-char Git SHA provenance, explicit SPDX license clearance, and explicit order-path containment policy.
- Unlicensed (`NONE`), archived, and strong-copyleft (`GPL-3.0`) repositories are explicitly fenced into `LICENSE_AND_ARCHIVE_QUARANTINE_WATCHLIST`, preventing license contamination or stale upstream drift.
