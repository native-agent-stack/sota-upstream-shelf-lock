"""Verify ADR-0019 upstream indicator & charting primitive provenance parity."""

from __future__ import annotations

import json
import pathlib

from shelf_lock import load_pins_lock

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

EXPECTED_CANONICAL_STRATEGIES = {
    "Strategy_1_Zarattini_2024_StocksInPlay_ORB.pine",
    "Strategy_2_Zarattini_2025_NoiseArea_VWAP.pine",
    "Strategy_3_Stockbee_MomentumBurst_EP.pine",
    "Strategy_4_Minervini_VCP_&_Qullamaggie_Short.pine",
    "Strategy_5_BJZZ_InstDarkSweep_OFI_PassiveBid.pine",
    "Strategy_6_VIX_TermStructure_Regime_Surfer.pine",
    "SOTA_Early_Mover_Bracket_Strategy.pine",
}


def test_adr0019_upstream_indicator_and_charting_primitives_parity() -> None:
    catalog = json.loads((REPO_ROOT / "STARRED_CONVERGENCE_CATALOG.json").read_text(encoding="utf-8"))
    pins_doc = load_pins_lock(REPO_ROOT)
    pins = {p["name"]: p for p in pins_doc["upstreamShelfPins"]}

    assert len(pins) == 18
    block = catalog["upstreamIndicatorAndChartingPrimitives"]
    assert block["schemaId"] == "sota-v3112-upstream-indicator-primitives.v1"
    assert block["adr"] == "ADR-0019"
    assert block["immutableCorePinsUntouched"] == 18
    assert block["orderAuthority"] is False
    assert block["visualArtifactsMayBindAlertOrWebhook"] is False
    assert block["takeProfitCapEnabled"] is False
    assert block["standaloneAlphaClaim"] is False
    assert block["promotionTrack"] == "PROTECTIVE_FILTER_OR_GOVERNANCE"

    live_ports = set(block["livePortsRefused"])
    assert live_ports == {4001, 7496, 8796, 8798}
    assert live_ports.isdisjoint({8799, 8787, 8797, 4002, 8794, 8792})
    assert block["liveHostsRefused"] == ["api.alpaca.markets"]

    raw_sources = block["pinnedIndicatorSources"]
    source_names = [s["pinName"] for s in raw_sources]
    assert len(source_names) == len(set(source_names)), "Duplicate pinnedIndicatorSources entry"
    sources = {s["pinName"]: s for s in raw_sources}
    assert set(sources) == {"nautilus_trader", "hftbacktest", "lightweight-charts", "perspective"}
    for name, entry in sources.items():
        pin = pins[name]
        assert entry["commit"] == pin["commit"] and len(entry["commit"]) == 40
        assert entry["ref"] == pin["ref"]
        assert entry["license"] == pin["license"]
        assert entry["orderAuthority"] is False

    nautilus = sources["nautilus_trader"]
    assert nautilus["nativeRustIndicatorsVerified"] == 39
    assert any("crates/indicators/src/ratio/spread_analyzer.rs" in f for f in nautilus["parityFormulas"])

    hft = sources["hftbacktest"]
    assert any(
        "queue.rs" in f and "lot-rounded" in f and "print-eligibility" in f for f in hft["parityFormulas"]
    )
    assert all(
        "spread cap" not in f.lower() and "fill probability" not in f.lower() for f in hft["parityFormulas"]
    )

    lwc = sources["lightweight-charts"]
    assert lwc["officialPluginsVerified"] == 29
    # Verify deployed npm 5.0.8 commit matches the catalog's own ADR-0017 dual-asset release pin byte-for-byte!
    lwc_prov = catalog["terminalPlatformTaxonomy"]["chartAssetProvenance"]
    expected_508_commit = lwc_prov["deployedReleaseCommit"]
    assert lwc["deployedNpmAsset"]["version"] == lwc_prov["deployedVersion"] == "5.0.8"
    assert lwc["deployedNpmAsset"]["commit"] == expected_508_commit
    assert len(expected_508_commit) == 40
    assert set(lwc["parityPrimitives"]) == {
        "volume-profile",
        "session-highlighting",
        "bands-indicator",
        "user-price-lines",
        "delta-tooltip",
    }

    strat_list = block["canonicalPineV6Strategies"]
    assert len(strat_list) == len(set(strat_list)) == 7
    assert set(strat_list) == EXPECTED_CANONICAL_STRATEGIES
    assert block["canonicalMasterIndicator"] == "SOTA_Master_All_In_One_24x5_Indicator.pine"

    # When the immutable upstream shelf is mounted on this workstation, verify exact counts on disk!
    upstream_root = pathlib.Path.home() / "Documents" / "upstream"
    nt_ind_src = upstream_root / "nautilus_trader" / "crates" / "indicators" / "src"
    if nt_ind_src.is_dir():
        native_rs = [
            p
            for p in nt_ind_src.rglob("*.rs")
            if "python" not in p.parts
            and "impl Indicator for " in p.read_text(encoding="utf-8", errors="ignore")
        ]
        assert len(native_rs) == nautilus["nativeRustIndicatorsVerified"]
    lwc_plugins = upstream_root / "lightweight-charts" / "plugin-examples" / "src" / "plugins"
    if lwc_plugins.is_dir():
        plugin_dirs = [p for p in lwc_plugins.iterdir() if p.is_dir()]
        assert len(plugin_dirs) == lwc["officialPluginsVerified"]
