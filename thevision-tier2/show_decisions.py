"""
show_decisions.py
Displays the Fleet General's AI reasoning from the last run.
Usage: python3 show_decisions.py
"""

import json
import os

PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "generated",
    "fleet_log.json"
)

def main():
    try:
        data = json.load(open(PATH))
    except FileNotFoundError:
        print("No fleet_log.json found. Run python3 run_fleet.py --demo first.")
        return

    decisions = data.get("decisions", [])
    state     = data.get("mission_state", {})

    print()
    print("=" * 62)
    print("  FLEET GENERAL — LIVE AI DECISIONS")
    print("=" * 62)
    print()
    print(f"  Mission: {state.get('objective', '')[:60]}")
    print(f"  Actor:   {state.get('actor', '')}")
    print(f"  Status:  {state.get('status', '')}")
    print(f"  Agents:  {state.get('active_agents', [])}")
    print()
    print("=" * 62)
    print()

    for i, d in enumerate(decisions, 1):
        dec = d.get("decision", {})
        print(f"  Decision {i}: {d.get('situation', '').upper()}")
        print(f"  Action:  {dec.get('decision', '')[:80]}")
        print(f"  SPARTA:  {dec.get('sparta_mapping', '')}")
        print(f"  Crew:    {dec.get('crew_safety_impact', '').upper()}")
        print(f"  Reason:  {dec.get('reasoning', '')[:120]}")
        agents = dec.get("next_actions", [])
        if agents:
            print(f"  Tasked:  {[a.get('agent') for a in agents]}")
        print()
        print("  " + "-" * 58)
        print()

    sparta = state.get("sparta_mappings", {})
    if sparta:
        print("  SPARTA COVERAGE")
        for ttp in sparta.keys():
            print(f"    {ttp}")
        print()

    print(f"  Total findings: {len(state.get('findings', []))}")
    print()
    print("=" * 62)
    print()

if __name__ == "__main__":
    main()
