"""
aegis.py

Single entrypoint for the full AEGIS pipeline.

Usage:
    python3 aegis.py
    python3 aegis.py --scenario scenarios/nation_state_capture.yaml
    python3 aegis.py --scenario scenarios/supply_chain_vendor.yaml
    python3 aegis.py --scenario scenarios/insider_ground_ops.yaml

What it does:
    1. Loads SPARTA knowledge base
    2. Generates AI attack chain for scenario
    3. Executes chain against Docker lab
    4. Runs AI gap analysis
    5. Generates SPARTA heatmap
    6. Writes AI engagement debrief
    7. Prints summary
"""

import os
import sys
import json
import time
import subprocess
import argparse

BASE = "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"

def banner():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        AEGIS — Haven-1 Adversary Simulation Engine           ║")
    print("║        AI-Driven SPARTA Emulation & Gap Identification       ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

def step(num: int, total: int, label: str):
    print(f"[{num}/{total}] {label}...")

def run(cmd: list, label: str) -> bool:
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def check_lab() -> bool:
    """Check Docker lab is running."""
    import urllib.request
    try:
        urllib.request.urlopen(
            "http://localhost:8080/health", timeout=3
        )
        return True
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="AEGIS — Haven-1 Simulation")
    parser.add_argument(
        "--scenario",
        default=f"{BASE}/scenarios/nation_state_capture.yaml",
        help="Path to scenario YAML file"
    )
    parser.add_argument(
        "--skip-runner",
        action="store_true",
        help="Skip execution runner (use existing results.json)"
    )
    args = parser.parse_args()

    CHAIN   = f"{BASE}/generated/chain.json"
    RESULTS = f"{BASE}/generated/results.json"
    GAPS    = f"{BASE}/generated/gap_report.json"
    HEATMAP = f"{BASE}/generated/heatmap.html"
    DEBRIEF = f"{BASE}/generated/debrief.md"
    RUNNER  = f"{BASE}/runner/aegis-runner"

    banner()

    scenario_name = os.path.basename(args.scenario).replace(".yaml", "")
    print(f"  Scenario:  {scenario_name}")
    print(f"  SPARTA:    v3.2 (seed data)")
    print(f"  Lab:       http://localhost:808x")
    print()

    total_steps = 6
    start = time.time()

    # ── Step 1 — Check lab ──────────────────────────────────────────
    step(1, total_steps, "Checking Docker lab")
    if check_lab():
        print("  Lab: all containers healthy")
    else:
        print("  Lab: containers not responding")
        print("  Run: cd lab && docker compose up -d")
        print("  Then wait 8 seconds and retry")
        sys.exit(1)
    print()

    # ── Step 2 — Generate attack chain ─────────────────────────────
    step(2, total_steps, "Generating AI attack chain")
    ok = run([
        "python3", f"{BASE}/planner/chain_builder.py"
    ], "chain builder")
    if not ok:
        print("  Chain builder failed — check ANTHROPIC_API_KEY")
        sys.exit(1)
    print()

    # ── Step 3 — Execute chain ──────────────────────────────────────
    if not args.skip_runner:
        step(3, total_steps, "Executing attack chain against lab")
        ok = run([RUNNER, CHAIN], "execution runner")
        if not ok:
            print("  Runner failed")
            sys.exit(1)
    else:
        print(f"[3/{total_steps}] Skipping runner — using existing results")
    print()

    # ── Step 4 — Gap analysis ───────────────────────────────────────
    step(4, total_steps, "Running AI gap analysis")
    ok = run([
        "python3", f"{BASE}/analysis/gap_analyzer.py", RESULTS
    ], "gap analyzer")
    if not ok:
        print("  Gap analyzer failed")
        sys.exit(1)
    print()

    # ── Step 5 — Heatmap ────────────────────────────────────────────
    step(5, total_steps, "Rendering SPARTA heatmap")
    ok = run([
        "python3", f"{BASE}/outputs/heatmap.py"
    ], "heatmap")
    if not ok:
        print("  Heatmap failed")
        sys.exit(1)
    print()

    # ── Step 6 — Debrief ────────────────────────────────────────────
    step(6, total_steps, "Writing AI engagement debrief")
    ok = run([
        "python3", f"{BASE}/outputs/debrief_writer.py",
        RESULTS, GAPS
    ], "debrief writer")
    if not ok:
        print("  Debrief writer failed")
        sys.exit(1)
    print()

    # ── Summary ─────────────────────────────────────────────────────
    elapsed = time.time() - start

    # Load results for summary
    try:
        with open(RESULTS) as f:
            results = json.load(f)
        with open(GAPS) as f:
            gaps = json.load(f)

        passed = results.get("steps_passed", 0)
        failed = results.get("steps_failed", 0)
        total_gaps = gaps.get("total_gaps_found", 0)
        top_cm = gaps.get("top_countermeasure", "N/A")
        top_data = next(
            (c for c in gaps.get("ranked_countermeasures", [])
             if c["cm_id"] == top_cm), {}
        )

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print()
        print("  AEGIS COMPLETE")
        print()
        print(f"  Steps passed:     {passed}")
        print(f"  Steps failed:     {failed}")
        print(f"  Gaps identified:  {total_gaps}")
        print(f"  Top fix:          {top_cm}")
        if top_data:
            print(f"  Chains blocked:   {top_data.get('chains_blocked', 0)}")
            print(f"  Crew safety:      {top_data.get('max_crew_safety_weight', 0)}/10")
        print(f"  Runtime:          {elapsed:.1f}s")
        print()
        print(f"  Heatmap:  {HEATMAP}")
        print(f"  Debrief:  {DEBRIEF}")
        print(f"  Gaps:     {GAPS}")
        print()
        print("  Opening heatmap in browser...")
        os.system(f'open "{HEATMAP}"')
        print()

    except Exception as e:
        print(f"  Could not load summary: {e}")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()


if __name__ == "__main__":
    main()
