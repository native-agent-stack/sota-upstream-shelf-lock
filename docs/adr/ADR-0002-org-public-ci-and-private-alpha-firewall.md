# ADR-0002: Public Unlimited-CI Control Plane vs Private Alpha & Execution Firewall Inside `native-agent-stack`

- **Status:** Accepted
- **Date:** 2026-11-17
- **Evidence Grade:** E3 (Cross-Family Council + Privacy Scanner Enforced)

## Context and Problem Statement

Running continuous multi-model CI (`ruff`, `ty`, `pytest`, Hypothesis property fuzzing, ADR zero-drift, and upstream SHA attestation) benefits from GitHub's unlimited free Actions minutes on public repositories, whereas live alpha weights, factor tuning manifests, empirical lake reports, and Alpaca/IBKR execution engines must remain strictly private.

## Decision Outcome

Partition [`native-agent-stack`](https://github.com/native-agent-stack) into two runtime-verified tiers:
1. **Public Infrastructure & CI Tier:** `.github`, `native-agent-stack`, `sota-upstream-shelf-lock`, `sota-multi-model-workflows`, `sota-compounding-lab`, `sota-harness-foundation`, `agy-sota-harness`, and `dsh-sota-harness` (`0` secrets, `0` local home paths, `0` proprietary weights).
2. **Private Alpha, Simulation & Execution Tier:** `meridian` (`Sim`), `sota-mover-ranker` (`Paper/Radar`), `sota-dynamic-trail-c` (`24/5 Guardian`), `cc-sota-harness` (`H05` lake empirical audit), `sota-private-vault`, and `ecosystem-records`.
