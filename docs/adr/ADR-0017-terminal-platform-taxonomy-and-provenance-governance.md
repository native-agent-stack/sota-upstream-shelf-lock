# ADR-0017: Terminal & Platform Four-Class Capability Taxonomy and Dual Asset Provenance Governance

- **Status:** Accepted
- **Date:** 2026-11-19
- **Evidence Grade:** E3
- **GitHub Evidence:** https://github.com/tradingview/lightweight-charts/blob/c29c51e1e5bc61981da5832c97797cb8283d120f/package.json, https://github.com/tradingview/lightweight-charts/tree/c65d0697ad0c546301a1734912ca50d031d468a2, https://github.com/perspective-dev/perspective/tree/0264ec13cd28ef4a2a136c8ef021c3c112bc8990, https://github.com/nautechsystems/nautilus_trader/tree/da6b57aefdd62b44f675e434ffcfefca7f4025dd, https://github.com/nkaz001/hftbacktest/tree/5f3ec40b2afb764e0fea112f941ed85523ef4e88, https://github.com/Fincept-Corporation/FinceptTerminal, https://github.com/flowsurface-rs/flowsurface, https://github.com/QuantConnect/Lean, https://github.com/openbq-org/OpenBB

## Context and Problem Statement

The cockpit, research and execution repositories of `native-agent-stack` borrow from many trading terminals and platforms. Until now no single record said which of them may be integrated, which may only inspire independently re-derived patterns, which may run beside the core with zero order authority, and which are refused outright. Two rehearsals for the `v3.10.11` wave (Seat E0 architecture spec §3.1/§5 and Seat E5 landscape audit) used different class names, and Seat E5 proposed restating every platform row inside the org manifest, which would create two drifting copies.

Two provenance facts also need a permanent home, because a single-version description of either asset is untrue:

- **Lightweight Charts.** The `PINS_LOCK.json` shelf commit `c29c51e1e5bc61981da5832c97797cb8283d120f` (`master`) declares package version `5.3.0`. The asset the ranker deploys is the published npm `5.0.8` standalone JS, byte-for-byte: tag `v5.0.8` peels to `c65d0697ad0c546301a1734912ca50d031d468a2`, and the deployed file hashes to SHA-256 `bcdca2a528db7c9b386918c99c544bde3eda3f0204ec2d23a64411d4cb4686c9`. "Lightweight Charts v5" names a major line, not a pin.
- **Perspective.** `PINS_LOCK.json` cites `https://github.com/finos/perspective` at `v5.9.2` / `0264ec13cd28ef4a2a136c8ef021c3c112bc8990`. The runtime npm scope is `@perspective-dev/*` (`5.9.2`), and workflows `ADR-0035` (in `sota-multi-model-workflows`) cites `perspective-dev/perspective`. Both are recorded; neither is picked by guess.

## Decision Outcome

1. **This ADR is the single canonical owner of the taxonomy.** The classes, their predicates and one row per named surface live only in the additive `terminalPlatformTaxonomy` block of `STARRED_CONVERGENCE_CATALOG.json` (schema id `sota-terminal-platform-taxonomy.v1`). Downstream manifests (org `ADR-0036`, umbrella `ADR-0039`) carry a pointer only: this repo's commit, the schema id, row counts and the SHA-256 of the canonical block (`json.dumps(block, sort_keys=True, separators=(",", ":"))`). Classification is by capability, because one vendor can sit in two classes.

2. **Four classes, each with a test-checkable predicate:**

   | Class | Predicate |
   | --- | --- |
   | `PINNED_INTEGRATE` | Present in `PINS_LOCK.json` with a 40-hex commit and an allowed licence. Any deployed or vendored asset records its own version next to the pin. |
   | `PHILOSOPHY_ONLY` | No runtime import, vendored code or asset, account, feed, network call or lockfile entry. Only independently re-derived maths or interaction patterns. |
   | `OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH` | Separate process or display with zero order authority, not imported by core packages; every core test passes with it absent. Its authority over the core stays `PHILOSOPHY_ONLY`. |
   | `HARD_REFUSED_EXECUTION_SAAS` | Any path where a third-party hosted service or third-party application holds broker access or relays a signal to a broker. Refused before dispatch, in paper and live alike. |

3. **Fourteen named surfaces** (4 + 7 + 2 + 1):

   | # | Surface | Class | Recorded scope |
   | --- | --- | --- | --- |
   | 1 | `perspective` | `PINNED_INTEGRATE` | `v5.9.2` @ `0264ec13cd28ef4a2a136c8ef021c3c112bc8990` (Apache-2.0) |
   | 2 | `lightweight-charts` | `PINNED_INTEGRATE` | `master` @ `c29c51e1e5bc61981da5832c97797cb8283d120f` (Apache-2.0) |
   | 3 | `nautilus_trader` | `PINNED_INTEGRATE` | `v2.0.0rc9` @ `da6b57aefdd62b44f675e434ffcfefca7f4025dd` (LGPL-3.0-or-later) |
   | 4 | `hftbacktest` | `PINNED_INTEGRATE` | `main` @ `5f3ec40b2afb764e0fea112f941ed85523ef4e88` (MIT) |
   | 5 | TrendSpider | `PHILOSOPHY_ONLY` | Split-Half Intrabar VWAP and Catalyst-Anchored VWAP, re-derived locally |
   | 6 | Bookmap | `PHILOSOPHY_ONLY` | L2 resting-depth heatmap and inferred absorption |
   | 7 | Sierra Chart | `PHILOSOPHY_ONLY` | High-density native desktop study layout |
   | 8 | DAS Trader Pro | `PHILOSOPHY_ONLY` | Hotkey staged-bracket ergonomics (stage and validate only) |
   | 9 | QuantConnect / LEAN | `PHILOSOPHY_ONLY` | Corporate-action and point-in-time universe-membership fixtures |
   | 10 | FinceptTerminal | `PHILOSOPHY_ONLY` | Design reference only; `AGPL-3.0` is outside `ALLOWED_LICENSES` |
   | 11 | Flowsurface | `PHILOSOPHY_ONLY` | Rust/Canvas historical DOM and time-and-sales strip; `GPL-3.0` is outside `ALLOWED_LICENSES` |
   | 12 | TradingView Desktop | `OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH` | `DISPLAY1` one-way visual lens (workflows `ADR-0035`); core authority stays `PHILOSOPHY_ONLY` |
   | 13 | OpenBB Platform / Workspace | `OPTIONAL_READ_ONLY_OR_OFFLINE_RESEARCH` | Isolated offline Python/MCP research sidecar; core authority stays `PHILOSOPHY_ONLY` |
   | 14 | SignalStack | `HARD_REFUSED_EXECUTION_SAAS` | Hosted alert-to-broker relay |

   The other 14 locked pins in `PINS_LOCK.json` are also `PINNED_INTEGRATE`; the block lists them by name only, and their commits stay owned by `PINS_LOCK.json`. Closed-source vendors (TrendSpider, Bookmap, Sierra Chart, DAS Trader Pro, TradingView, SignalStack) are listed by class and predicate only, with zero version or feature claims. The existing catalog anchors `QuantConnect/Lean` and `openbq-org/OpenBB` keep `authority: PHILOSOPHY_ONLY` unchanged; the `OPTIONAL_*` class governs only the out-of-band process or display.

4. **Hard-refused execution routes.** SignalStack and TrendSpider + SignalStack relays; TradingView alert-to-webhook order bridges where a third-party relay or hosted service reaches a broker; TradingView broker-connected chart trading; unguarded chart-click orders; closed SaaS execution relays; QuantConnect cloud live deployment. Live ports `4001`, `7496`, `8796`, `8798` and every host in `PINS_LOCK.json#/invariants/forbiddenLiveHosts` are refused. The block's live-port list is a strict superset of `PINS_LOCK.json#/invariants/forbiddenLivePorts` (`[4001, 7496]`), and it is disjoint from the loopback paper ports `4002`, `8787`, `8797`, `8799`.

5. **First-party paper bridge sits outside all four classes, pending decision D7.** A first-party chart-alert bridge into the P1 paper lane's own gates is landed code, owned by `sota-dynamic-trail-c`. The refused class therefore names third-party relays that reach a broker, not "every TradingView webhook". No artifact classified as a visual surface may be bound to an alert or webhook. Retiring or reclassifying the bridge belongs to a `sota-dynamic-trail-c` ADR, not this one.

6. **Promotion boundary notes.** The taxonomy grants no promotion-stage elevation. Where it interacts with the promotion gate, the executable boundary in `src/shelf_lock/validator.py` is authoritative:
   - **HLZ calling convention:** shelf-lock takes the candidate-inclusive trial count. With 103 completed ledger trials, the next candidate is evaluated as `cumulative_trials_n=104`, so `t*(104) = 4.2063`. Passing `103` reproduces the prior hurdle `4.2041`.
   - **DSR:** a candidate passes only if `dsr > 0.95`; `DSR == 0.95` is rejected.
   - **PBO:** a candidate passes only if `pbo < 0.25`; `PBO >= 0.25` is rejected.

7. **No pin changes.** `PINS_LOCK.json` stays at 18 pins with unchanged URLs, including `finos/perspective`. The catalog's root `schemaVersion` (`sota-starred-convergence.v3.10.8`), root `authority`, every existing anchor's `authority`, the `415`/`8`/`18` counts and `beyond_starred_sota_additions` are unchanged.

## Alternatives Considered

- **Restate the platform rows in the org manifest (Seat E5 rehearsal).** Rejected: two copies of the rows would drift. The org manifest pins this block by commit and SHA-256 instead.
- **Name the third class `OPTIONAL_OFFLINE_RESEARCH`.** Rejected: the TradingView lens is an online display, so the name would be untrue.
- **Refuse every TradingView webhook.** Rejected for this wave: it would contradict the landed first-party paper bridge and the ranker template validator's `paper_only` confirmed-bar webhook payload (decision D7).
- **Rewrite the Perspective pin URL to `perspective-dev/perspective`.** Deferred: pins are immutable here; the rename is recorded as a dated observation, and any URL change needs its own pin ADR.
- **Bump the catalog `schemaVersion`.** Rejected: the block carries its own schema id, and existing tests pin the root version.

## Verification Witness

- **Re-read at GitHub on 2026-11-19 (this ADR):** `tradingview/lightweight-charts` `package.json` at `c29c51e1` declares `"version": "5.3.0"`; annotated tag `v5.0.8` peels to `c65d0697ad0c546301a1734912ca50d031d468a2`. `finos/perspective` resolves to `perspective-dev/perspective` (Apache-2.0), and annotated tag `v5.9.2` peels to `0264ec13cd28ef4a2a136c8ef021c3c112bc8990`. `Fincept-Corporation/FinceptTerminal` licence `AGPL-3.0`; `flowsurface-rs/flowsurface` licence `GPL-3.0`; `QuantConnect/Lean` licence `Apache-2.0`. `OpenBB-finance/OpenBB` resolves to `openbq-org/OpenBB`.
- **Carried from the Seat E5 landscape audit (not re-hashed here):** the ranker's vendored standalone JS and the file inside the published npm `lightweight-charts@5.0.8` tarball both hash to SHA-256 `bcdca2a528db7c9b386918c99c544bde3eda3f0204ec2d23a64411d4cb4686c9`, and the tarball passed its npm SHA-512 integrity check.
- **Local:** `compute_hlz_t_hurdle(104) == 4.2063` and `compute_hlz_t_hurdle(103) == 4.2041`; `validate_promotion_candidate` rejects `dsr_probability == 0.95` and `cpcv_pbo == 0.25`. New semantic tests in `tests/test_shelf_lock.py` cover the schema id, the four classes, the 14 surfaces, pin parity by name and commit, both provenance records, the FinceptTerminal licence, port disjointness and anchor authority.
- **Gates:** `python scripts/architecture_catalog.py --check` (`17` ADRs, `0` drift), `uv run --extra dev pytest`, `ruff check .`, `ruff format --check .`, `scan_repo_privacy_hygiene` and `gitleaks` on staged changes.

## Rollback

Revert the single commit that introduced this ADR. The block is additive and consumers pin it by commit and SHA-256, so nothing downstream breaks; re-seal any downstream pointer in reverse landing order.
