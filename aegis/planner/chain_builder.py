"""
planner/chain_builder.py

Calls the Claude API to generate a SPARTA-mapped attack chain
given a scenario YAML and the SPARTA knowledge base.

Component 1 of AEGIS — the AI mission planner.
"""

import json
import os
import yaml
import anthropic

from sparta.parser import SPARTAKnowledgeBase
from planner.prompts import HAVEN1_ARCHITECTURE, CHAIN_BUILDER_SYSTEM


def load_scenario(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def build_chain(
    scenario: dict,
    kb: SPARTAKnowledgeBase,
    verbose: bool = True
) -> dict:
    """
    Call Claude API to generate an attack chain for the scenario.

    Returns parsed chain dict with steps, TTP IDs, and metadata.
    """
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    actor = scenario.get("actor", "nation-state APT")
    target = scenario.get("target", "Haven-1 ground segment")
    objective = scenario.get("objective", "capture Haven-1")

    if verbose:
        print(f"[PLANNER] Generating attack chain")
        print(f"  Actor:     {actor}")
        print(f"  Target:    {target}")
        print(f"  Objective: {objective}")
        print(f"[PLANNER] Calling Claude API...")

    user_prompt = f"""
Generate a realistic SPARTA-mapped attack chain for this scenario.

THREAT ACTOR: {actor}
TARGET ENVIRONMENT: {target}
OBJECTIVE: {objective}

HAVEN-1 ARCHITECTURE:
{HAVEN1_ARCHITECTURE}

SPARTA KNOWLEDGE BASE — use only these TTP IDs:
{kb.summary_for_prompt()}

REQUIREMENTS
- Complete end-to-end chain from initial access to objective
- Only use SPARTA TTP IDs listed above
- Realistic operational order — recon before exploitation
- Passive techniques before active techniques
- Each step builds on the previous step
- Assign crew_safety_impact per step
- Reference Haven-1 specific systems where applicable

Respond with raw JSON only. No explanation. No markdown.
"""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=CHAIN_BUILDER_SYSTEM,
        messages=[{"role": "user", "content": user_prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown if Claude wraps the response
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    chain = json.loads(raw)

    if verbose:
        steps = chain.get("chain", [])
        print(f"[PLANNER] Chain generated — {len(steps)} steps")
        print()
        for step in steps:
            impact = step.get("crew_safety_impact", "unknown")
            print(f"  Step {step['step']:02d}  "
                  f"{step['ttp_id']:<14}  "
                  f"{step['name']:<35}  "
                  f"crew impact: {impact}")

    return chain


def save_chain(chain: dict, path: str = "generated/chain.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(chain, f, indent=2)
    print(f"\n[PLANNER] Chain saved to {path}")


if __name__ == "__main__":
    kb = SPARTAKnowledgeBase().load()

    scenario_path = "scenarios/nation_state_capture.yaml"

    if not os.path.exists(scenario_path):
        print(f"[PLANNER] Scenario not found at {scenario_path}")
        print("[PLANNER] Using default test scenario...")
        scenario = {
            "actor": "nation-state APT",
            "target": "Haven-1 ground segment and flight software",
            "objective": "capture Haven-1 and bring under foreign control"
        }
    else:
        scenario = load_scenario(scenario_path)
        print(f"[PLANNER] Loaded scenario: {scenario_path}")

    chain = build_chain(scenario, kb)
    save_chain(chain)

    print("\n--- Full chain detail ---")
    for step in chain.get("chain", []):
        print(f"\nStep {step['step']}: [{step['ttp_id']}] {step['name']}")
        print(f"  Action:     {step['action']}")
        print(f"  Detection:  {step['detection_opportunity']}")
        print(f"  Crew:       {step['crew_safety_impact']}")
