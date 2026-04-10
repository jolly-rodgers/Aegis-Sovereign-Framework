"""
analysis/gap_analyzer.py

Reads results.json from the execution runner and calls
the Claude API for each successful attack step.

For each step Claude identifies:
  - Which SPARTA countermeasures were absent
  - The NIST 800-53 control that maps to each gap
  - Crew safety weight (1-10)
  - The specific fix

This is Component 3 of AEGIS — the AI analysis loop.
"""

import json
import os
import anthropic
from sparta.parser import SPARTAKnowledgeBase
from planner.prompts import GAP_ANALYZER_SYSTEM, HAVEN1_ARCHITECTURE


def load_results(path: str = "generated/results.json") -> dict:
    with open(path) as f:
        return json.load(f)


def analyze_step(
    step: dict,
    kb: SPARTAKnowledgeBase,
    client: anthropic.Anthropic,
    verbose: bool = True
) -> dict:
    """
    Call Claude to analyze a single successful attack step.
    Returns structured gap analysis with CMs and fixes.
    """
    ttp_id = step.get("ttp_id", "")
    name = step.get("name", "")
    crew_impact = step.get("crew_safety_impact", "unknown")

    if verbose:
        print(f"\n[GAP] Analyzing Step {step['step']}: "
              f"[{ttp_id}] {name}")
        print(f"[GAP] Crew safety impact: {crew_impact}")

    # Get technique details from KB
    technique = kb.get(ttp_id)
    tech_context = ""
    if technique:
        tech_context = (
            f"Technique: {technique.name}\n"
            f"Description: {technique.description}\n"
            f"Known countermeasures: {', '.join(technique.countermeasures)}\n"
            f"NIST controls: {', '.join(technique.nist_controls)}\n"
            f"Haven-1 context: {technique.haven1_context}"
        )

    user_prompt = f"""
A nation-state APT successfully executed this attack step
against Haven-1 crewed space station:

STEP: {step['step']}
SPARTA TTP: {ttp_id}
TECHNIQUE: {name}
CREW SAFETY IMPACT: {crew_impact}

TECHNIQUE DETAILS:
{tech_context}

HAVEN-1 ARCHITECTURE:
{HAVEN1_ARCHITECTURE}

This step SUCCEEDED — meaning the security controls that
should have prevented it were absent or insufficient.

Identify every missing countermeasure. For each gap:
1. Which SPARTA countermeasure ID was absent (CM####)
2. What specifically was missing from Haven-1's defenses
3. The NIST 800-53 Rev 5 control that addresses this
4. Crew safety weight 1-10 (10 = crew survival critical)
5. The specific actionable fix Vast should implement

Be specific to Haven-1's actual architecture — AWS GovCloud,
Okta SSO, Jenkins CI/CD, NASA cFS, CryptoLib, Modbus OT.

Respond with raw JSON only. No explanation. No markdown.
"""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=GAP_ANALYZER_SYSTEM,
        messages=[{"role": "user", "content": user_prompt}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        analysis = json.loads(raw)
    except json.JSONDecodeError:
        analysis = {
            "step": step["step"],
            "ttp_id": ttp_id,
            "gaps": [],
            "overall_risk": "unknown",
            "parse_error": raw[:200]
        }

    if verbose:
        gaps = analysis.get("gaps", [])
        risk = analysis.get("overall_risk", "unknown")
        print(f"[GAP] Overall risk: {risk.upper()}")
        print(f"[GAP] Gaps identified: {len(gaps)}")
        for gap in gaps:
            print(f"  {gap.get('cm_id','?'):10}  "
                  f"weight:{gap.get('crew_safety_weight','?'):2}  "
                  f"{gap.get('description','')[:60]}")

    return analysis


def score_countermeasures(all_gaps: list[dict]) -> list[dict]:
    """
    Rank countermeasures by priority score.

    priority = chains_blocked x crew_safety_weight

    This tells engineering which fix to implement first —
    the one that breaks the most chains and protects
    the highest-criticality subsystem.
    """
    cm_scores = {}

    for step_analysis in all_gaps:
        for gap in step_analysis.get("gaps", []):
            cm_id = gap.get("cm_id", "")
            if not cm_id:
                continue

            if cm_id not in cm_scores:
                cm_scores[cm_id] = {
                    "cm_id": cm_id,
                    "description": gap.get("description", ""),
                    "nist_control": gap.get("nist_control", ""),
                    "max_crew_safety_weight": 0,
                    "chains_blocked": 0,
                    "fix": gap.get("fix", ""),
                    "steps_affected": [],
                }

            weight = gap.get("crew_safety_weight", 0)
            step_num = step_analysis.get("step", 0)

            cm_scores[cm_id]["chains_blocked"] += 1
            cm_scores[cm_id]["steps_affected"].append(step_num)
            cm_scores[cm_id]["max_crew_safety_weight"] = max(
                cm_scores[cm_id]["max_crew_safety_weight"], weight
            )

    # Calculate priority score
    ranked = []
    for cm in cm_scores.values():
        cm["priority_score"] = (
            cm["chains_blocked"] * cm["max_crew_safety_weight"]
        )
        ranked.append(cm)

    ranked.sort(key=lambda x: x["priority_score"], reverse=True)
    return ranked


def save_gap_report(
    all_gaps: list[dict],
    ranked_cms: list[dict],
    path: str = "generated/gap_report.json"
):
    report = {
        "total_steps_analyzed": len(all_gaps),
        "total_gaps_found": sum(
            len(s.get("gaps", [])) for s in all_gaps
        ),
        "top_countermeasure": ranked_cms[0]["cm_id"] if ranked_cms else None,
        "ranked_countermeasures": ranked_cms[:10],
        "step_analyses": all_gaps,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[GAP] Report saved to {path}")
    return report


def print_summary(ranked_cms: list[dict]):
    print("\n" + "="*62)
    print("  GAP ANALYSIS COMPLETE — TOP COUNTERMEASURES")
    print("="*62)
    print(f"  {'Priority':<10} {'CM ID':<10} {'Chains':<8} "
          f"{'Weight':<8} Description")
    print("-"*62)
    for i, cm in enumerate(ranked_cms[:7], 1):
        print(f"  {i:<10} "
              f"{cm['cm_id']:<10} "
              f"{cm['chains_blocked']:<8} "
              f"{cm['max_crew_safety_weight']:<8} "
              f"{cm['description'][:35]}")
    print("="*62)
    if ranked_cms:
        top = ranked_cms[0]
        print(f"\n  Top fix: {top['cm_id']} — {top['description']}")
        print(f"  Blocks {top['chains_blocked']} attack chain steps")
        print(f"  Crew safety weight: {top['max_crew_safety_weight']}/10")
        print(f"\n  Fix: {top['fix'][:120]}")


if __name__ == "__main__":
    print("[GAP] AEGIS Gap Analyzer starting...")
    print("[GAP] Loading SPARTA knowledge base...")
    kb = SPARTAKnowledgeBase().load()

    print("[GAP] Loading execution results...")
    import sys
    results_path = sys.argv[1] if len(sys.argv) > 1 else "generated/results.json"
    results = load_results(results_path)
    steps = results.get("steps", [])
    passed = [s for s in steps if s.get("status") == "pass"]
    print(f"[GAP] Found {len(passed)} successful attack steps to analyze")

    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    all_gaps = []
    for step in passed:
        analysis = analyze_step(step, kb, client)
        all_gaps.append(analysis)

    print("\n[GAP] Scoring and ranking countermeasures...")
    ranked_cms = score_countermeasures(all_gaps)

    report = save_gap_report(all_gaps, ranked_cms)
    print_summary(ranked_cms)

    print(f"\n[GAP] Total gaps found: {report['total_gaps_found']}")
    print(f"[GAP] Top countermeasure: {report['top_countermeasure']}")
    print("\n[GAP] Next step: python3 outputs/debrief_writer.py")
