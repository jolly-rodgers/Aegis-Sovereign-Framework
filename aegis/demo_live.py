"""
demo_live.py

Live end-to-end AEGIS demonstration.
Connects to real Docker containers and runs the full kill chain.
Use this when you have time and the lab is running.
"""

import subprocess
import sys
import time
import os
import json
import urllib.request

BASE = "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
CHAIN = f"{BASE}/generated/chain.json"
RESULTS = f"{BASE}/generated/results.json"
GAPS = f"{BASE}/generated/gap_report.json"
RUNNER = f"{BASE}/runner/aegis-runner"

def clear():
    os.system("clear")

def banner():
    clear()
    print()
    print("  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║        AEGIS — Haven-1 Adversary Simulation Engine           ║")
    print("  ║        AI-Driven SPARTA Emulation & Gap Identification       ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print()

def check_lab():
    print("  [1/6] Checking Docker lab health...")
    services = {
        "ground-identity":   "http://localhost:8080/health",
        "ground-pipeline":   "http://localhost:8081/health",
        "space-obc":         "http://localhost:8082/health",
        "space-lifesupport": "http://localhost:8083/health",
        "ground-station":    "http://localhost:8084/health",
        "space-comms":       "http://localhost:8085/health",
    }
    all_healthy = True
    for name, url in services.items():
        try:
            urllib.request.urlopen(url, timeout=3)
            print(f"         {name:<20} OK")
        except Exception:
            print(f"         {name:<20} OFFLINE")
            all_healthy = False

    if not all_healthy:
        print()
        print("  Lab not fully running. Starting containers...")
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=f"{BASE}/lab",
            capture_output=True
        )
        print("  Waiting for containers to start...")
        time.sleep(8)
    else:
        print()
        print("  All containers healthy.")
    print()

def run_step(label, cmd, cwd=None):
    print(f"  {label}")
    result = subprocess.run(
        cmd,
        cwd=cwd or BASE,
        capture_output=False
    )
    return result.returncode == 0

def main():
    banner()
    print("  LIVE DEMONSTRATION — Real Docker targets, real AI analysis")
    print("  ─────────────────────────────────────────────────────────")
    print()

    check_lab()

    # Step 2 — Generate chain
    print("  [2/6] Generating AI attack chain...")
    print("        Claude reasoning over SPARTA KB + Haven-1 architecture")
    print()
    ok = run_step("", [sys.executable, f"{BASE}/planner/chain_builder.py"])
    if not ok:
        print("  Chain generation failed. Check ANTHROPIC_API_KEY.")
        sys.exit(1)
    print()

    # Step 3 — Execute runner
    print("  [3/6] Executing kill chain against live lab targets...")
    print()
    ok = run_step("", [RUNNER, CHAIN])
    if not ok:
        print("  Runner failed.")
        sys.exit(1)
    print()

    # Step 4 — Gap analysis
    print("  [4/6] Running AI gap analysis...")
    print("        Claude analyzing each step for missing countermeasures")
    print()
    ok = run_step("", [sys.executable, f"{BASE}/analysis/gap_analyzer.py", RESULTS])
    if not ok:
        print("  Gap analysis failed.")
        sys.exit(1)
    print()

    # Step 5 — Heatmap
    print("  [5/6] Rendering SPARTA coverage heatmap...")
    run_step("", [sys.executable, f"{BASE}/outputs/heatmap.py"])
    print()

    # Step 6 — Debrief
    print("  [6/6] Writing AI engagement debrief...")
    run_step("", [sys.executable, f"{BASE}/outputs/debrief_writer.py", RESULTS, GAPS])
    print()

    # OPA demo
    print("  ─────────────────────────────────────────────────────────")
    print("  LIVE POLICY GATE DEMO")
    print()
    subprocess.run(["bash", f"{BASE}/defensive/opa_demo.sh"])

    # Summary
    try:
        results = json.load(open(RESULTS))
        gaps = json.load(open(GAPS))
        passed = results.get("steps_passed", 0)
        total = passed + results.get("steps_failed", 0)
        total_gaps = gaps.get("total_gaps_found", 0)
        top_cm = gaps.get("top_countermeasure", "N/A")
        top_data = next(
            (c for c in gaps.get("ranked_countermeasures", [])
             if c["cm_id"] == top_cm), {}
        )
        print()
        print("  ─────────────────────────────────────────────────────────")
        print("  AEGIS LIVE RUN COMPLETE")
        print()
        print(f"  Steps passed:     {passed}/{total}")
        print(f"  Gaps identified:  {total_gaps}")
        print(f"  Top fix:          {top_cm}")
        print(f"  Chains blocked:   {top_data.get('chains_blocked', 0)}")
        print(f"  Crew safety:      {top_data.get('max_crew_safety_weight', 0)}/10")
        print()
        print(f"  Heatmap: {BASE}/generated/heatmap.html")
        print(f"  Debrief: {BASE}/generated/debrief.md")
        print()
        os.system(f'open "{BASE}/generated/heatmap.html"')
    except Exception as e:
        print(f"  Could not load summary: {e}")

if __name__ == "__main__":
    main()
