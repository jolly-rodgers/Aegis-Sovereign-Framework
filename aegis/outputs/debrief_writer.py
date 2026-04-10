"""
outputs/debrief_writer.py

Reads results.json and gap_report.json and calls Claude
to write a complete engagement debrief in plain English.

Readable by both security teams and engineering leadership.
Saved to generated/debrief.md
"""

import json
import os
import sys
import anthropic
from planner.prompts import DEBRIEF_WRITER_SYSTEM, HAVEN1_ARCHITECTURE


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def build_debrief_prompt(results: dict, gap_report: dict) -> str:
    steps_summary = []
    for step in results.get("steps", []):
        steps_summary.append(
            f"Step {step['step']}: [{step['ttp_id']}] {step['name']} "
            f"— {step['status'].upper()} "
            f"(crew impact: {step['crew_safety_impact']})"
        )

    top_cms = gap_report.get("ranked_countermeasures", [])[:7]
    cm_summary = []
    for cm in top_cms:
        cm_summary.append(
            f"{cm['cm_id']}: {cm['description'][:80]} "
            f"(blocks {cm['chains_blocked']} steps, "
            f"crew weight: {cm['max_crew_safety_weight']}/10)"
        )

    return f"""
Write a complete red team engagement debrief for Vast Space.

ENGAGEMENT SUMMARY
Actor:      {results.get('actor')}
Target:     {results.get('target')}
Objective:  {results.get('objective')}
Steps run:  {results.get('steps_passed', 0)} passed,
            {results.get('steps_failed', 0)} failed
Total gaps: {gap_report.get('total_gaps_found', 0)}

ATTACK CHAIN RESULTS
{chr(10).join(steps_summary)}

TOP COUNTERMEASURES MISSING
{chr(10).join(cm_summary)}

HAVEN-1 ARCHITECTURE CONTEXT
{HAVEN1_ARCHITECTURE}

Write a professional engagement debrief with these sections:

1. EXECUTIVE SUMMARY (3-4 sentences — what happened,
   what it means for the crew, what needs to happen first)

2. ATTACK NARRATIVE (plain English walkthrough of the
   full kill chain — written so a mission engineer
   understands exactly what happened and why it matters)

3. CRITICAL FINDINGS (top 5 gaps with specific technical
   detail — what was missing, what it enabled, crew impact)

4. HARDENING ROADMAP (top 7 countermeasures ranked by
   crew safety priority — specific actionable fixes with
   NIST control references)

5. PHYSICAL CREW CONTROLS (what the crew can do right now
   before software fixes are deployed — physical overrides,
   analog gauge cross-checks, emergency protocols)

6. CONCLUSION (one paragraph — how this changes the
   security posture for Haven-1 and what it means for
   Haven-2 and the Artificial Gravity Station program)

Tone: professional, direct, safety-focused.
This document will be read by Vast engineering leadership.
Format as clean markdown.
"""


def write_debrief(results: dict, gap_report: dict, verbose: bool = True) -> str:
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    if verbose:
        print("[DEBRIEF] Calling Claude to write engagement report...")
        print("[DEBRIEF] This takes 20-30 seconds...")

    prompt = build_debrief_prompt(results, gap_report)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=DEBRIEF_WRITER_SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )

    debrief = response.content[0].text
    return debrief


def save_debrief(debrief: str, path: str = "generated/debrief.md"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(debrief)
    print(f"[DEBRIEF] Report saved to {path}")


if __name__ == "__main__":
    base = "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"

    results_path = sys.argv[1] if len(sys.argv) > 1 else f"{base}/generated/results.json"
    gaps_path = sys.argv[2] if len(sys.argv) > 2 else f"{base}/generated/gap_report.json"
    output_path = f"{base}/generated/debrief.md"

    print("[DEBRIEF] Loading results...")
    results = load_json(results_path)
    print("[DEBRIEF] Loading gap report...")
    gap_report = load_json(gaps_path)

    debrief = write_debrief(results, gap_report)
    save_debrief(debrief, output_path)

    print("\n[DEBRIEF] Preview (first 800 chars):")
    print("-" * 62)
    print(debrief[:800])
    print("-" * 62)
    print(f"\n[DEBRIEF] Full report: {output_path}")
    print("[DEBRIEF] Next step: python3 outputs/heatmap.py")
