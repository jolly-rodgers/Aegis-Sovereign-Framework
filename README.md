# AEGIS — Sovereign Framework
### AI-Driven Adversary Emulation for Crewed Space Station Security

> Autonomous adversary simulation built against the Haven-1 threat model.  
> Mapped to SPARTA v3.2. Generates working fixes, not findings lists.  
> The foundation for an autonomous orbital security program.

[![SPARTA v3.2](https://img.shields.io/badge/Framework-SPARTA%20v3.2-blue)](https://sparta.aerospace.org)
[![Claude API](https://img.shields.io/badge/AI-Claude%20API-blueviolet)](https://anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Go 1.21+](https://img.shields.io/badge/Go-1.21%2B-cyan)](https://go.dev)

---

## What this is

AEGIS simulates a full nation-state attack chain against Haven-1's architecture, identifies every security gap, generates working fixes, and produces a prioritized hardening roadmap — all automatically. It is Tier 1 of a three-tier autonomous security program designed to scale with commercial crewed space operations through 2035.

This is not a scanner. It is not a compliance tool. It is an **adversary emulation engine** that reasons about your specific architecture, selects real attack techniques from SPARTA v3.2, executes them against an isolated digital twin, and delivers working code your engineering team can deploy the same day.

---

## The threat model

```
Actor:     Nation-state APT
Target:    Haven-1 — world's first commercial crewed space station
Objective: Station capture, not destruction

Why capture:
  Destruction creates debris and escalation.
  Capture creates a hostage situation, an intelligence windfall,
  and geopolitical leverage. Russia has already maneuvered assets
  into coplanar orbits with US government satellites.
  The capability and the intent exist.
```

Haven-1 is not a satellite. On a crewed vehicle, a successful cyberattack does not mean data loss — it means the crew cannot breathe, cannot communicate, or cannot come home.

---

## Quick start

```bash
# Clone and install dependencies
git clone https://github.com/jolly-rodgers/Aegis-Sovereign-Framework
cd Aegis-Sovereign-Framework

pip install anthropic networkx pyyaml rich pymodbus
go install ./aegis/runner/cmd/runner
brew install opa conftest          # macOS
export ANTHROPIC_API_KEY=sk-ant-...

# Run the primary scenario — nation-state APT, full kill chain
python3 aegis/aegis.py --scenario aegis/scenarios/nation_state_capture.yaml

# Start the Haven-1 digital twin lab
docker compose -f aegis/lab/docker-compose.yml up -d

# Run the Fleet General (multi-agent demo, no Docker required)
python3 thevision-tier2/run_fleet.py --demo

# Replay the General's reasoning decisions
python3 thevision-tier2/show_decisions.py
```

---

## The program — three tiers

```
TIER 1 — AEGIS                          Built · running today
─────────────────────────────────────────────────────────────
Single AI reasoning agent. Claude API over SPARTA v3.2.
Generates attack chain → executes against Haven-1 digital twin →
identifies gaps → produces working OPA policies, Sigma rules,
Terraform configs. One command, full pipeline, 47-second runtime.

  python3 aegis/aegis.py --scenario scenarios/nation_state_capture.yaml


TIER 2 — THE FLEET                      POC built · extending
─────────────────────────────────────────────────────────────
Autonomous multi-agent platform. The General reasons over SPARTA
v3.2 and assigns tasks to specialized agents. Attack and defense
fleets operate in parallel. General adapts mid-operation when
blocked. 4 agents built and demonstrated. 10 on the roadmap.

  python3 thevision-tier2/run_fleet.py --demo


TIER 3 — SOVEREIGN                      The destination
─────────────────────────────────────────────────────────────
A space station that defends itself. Detects threats without
ground intervention. Patches vulnerabilities in orbit without
a reboot. Cannot be captured, controlled, or coerced.

  Vast's mission is continuous human presence in space for
  America and its allies. A SOVEREIGN space station is one
  that cannot be taken from them.
```

---

## AEGIS — full kill chain

All techniques mapped to SPARTA v3.2. All steps executed against an isolated Docker lab. No production systems involved.

| Step | SPARTA ID | Technique | Result |
|------|-----------|-----------|--------|
| 1 | IA-0007 | Ground identity compromise via spearphishing | PASS |
| 2 | IA-0009.02 | CI/CD pipeline injection — XZ Utils technique on flight software | PASS |
| 3 | EX-0009 | OBC remote code execution, firmware-persistent implant | PASS |
| 4 | REC-0005 | Command intercept — 1,247 uplink commands captured passively | PASS |
| 5 | EX-0014.03 | Life support sensor spoofing — O₂ 20.9% reported / 14.2% actual | PASS ⚠ |
| 6 | EX-0001.01 | Station maneuver + comms cutoff via replayed commands | PASS |
| 7 | IMP-0002 | Station capture — docking system compromised, hatch opens | PASS ☠ |

**O₂ at 14.2%. Crew unaware. Ground ops blind.**

---

## THE FLEET — agent architecture

```
                    ┌─────────────────────────────┐
                    │         FLEET GENERAL        │
                    │  Live Claude API reasoning   │
                    │  SPARTA v3.2 · Haven-1 ctx   │
                    │  Assigns tasks · Adapts       │
                    │  Never executes directly      │
                    └──────────────┬──────────────┘
           ┌──────────────┬────────┴────────┬──────────────┐
           ▼              ▼                 ▼              ▼
     ATTACK FLEET    INTEL FLEET      DEFENSE FLEET
     ─────────────   ────────────     ─────────────
     ● Scout          ○ Mapper         ○ Medic
     ● Phantom         ○ Analyst        ○ Forge
     ● Breacher        ○ Oracle         ○ Sentinel
     ○ Wraith                           ○ Warden
     ○ Courier                          ○ Judge
     ○ Hammer

     ● Built & demonstrated    ○ Roadmap
```

### The General's actual reasoning — Haven-1 POC

These decisions were not scripted. The General received Scout's report and SPARTA v3.2. Crew safety was not mentioned in the prompt.

```
Decision 1 — Mission brief                              Crew: NONE
  "Phased approach. Begin recon. Establish full picture before
   any active steps."
   SPARTA: TA0001

Decision 2 — After Scout report                         Crew: MEDIUM
  "Dual-path attack strategy. Primary: IA-0007 ground identity
   exploiting MFA gaps. Secondary: EX-0009 CryptoLib fallback."

Decision 3 — After Phantom report                       Crew: HIGH
  "Signing key obtained. Advance to execution via supply chain.
   Task Breacher: exploit CVE-2025-29912."
   SPARTA: IA-0005 → EX-0009

Decision 4 — After Breacher report                      Crew: CRITICAL
  "CRITICAL MILESTONE. Implant confirmed. Task Wraith.
   Courier on standby. Hammer on standby.
   Implement strict operational boundaries to prevent
   crew safety incidents."
   SPARTA: PER-0003 → DE-0003 → IMP-0002
```

The crew safety flag emerged from reasoning — not from explicit instruction. The General understood what Haven-1 is.

---

## Outputs

AEGIS does not produce a findings list. It produces working code.

| Output | Description |
|--------|-------------|
| `generated/debrief.md` | Full engagement narrative — executive summary through per-TTP analysis |
| `generated/heatmap.html` | SPARTA matrix coverage map. Red = succeeded. Green = blocked. |
| `generated/roadmap.json` | Ranked countermeasure backlog with crew safety weights |
| `generated/policies/haven_update_policy.rego` | OPA/Conftest policy — blocks supply chain attack at CI/CD gate |
| `generated/sigma_rules/` | Detection rules for all observed TTPs, vendor-neutral |
| `generated/terraform/` | AWS hardening configs — MFA, IAM, encryption |

### OPA demo — one policy, two outcomes

```bash
# Without policy — attack succeeds
conftest test generated/policies/update_artifact.json
# PASS — artifact accepted (attack path open)

# Stage AEGIS-generated policy
cp generated/policies/haven_update_policy.rego policy/

# With policy — attack blocked
conftest test generated/policies/update_artifact.json --policy policy/
# FAIL — Update rejected: SBOM verification required
# FAIL — Update rejected: trusted key signature required
# FAIL — Update rejected: build provenance missing

# Clean artifact — passes
conftest test generated/policies/update_artifact_hardened.json --policy policy/
# PASS — all checks cleared
```

---

## Haven-1 digital twin

Six Docker containers. Two isolated networks. One command.

```bash
docker compose -f aegis/lab/docker-compose.yml up -d
```

```
Ground network              Space network
──────────────              ─────────────
haven-sso                   haven-obc
  Okta-style SSO              OBC · firmware write surface
  Phishable session tokens    Modbus register access

haven-cicd                  haven-lifesupport
  Jenkins pipeline            Modbus OT · O₂/CO₂/pressure
  Injectable build steps      Registers spoofable via implant

haven-uplink                haven-comms
  CCSDS telecommand           Downlink simulator
  Replay surface              Grafana + Loki telemetry
```

The network boundary between ground and space is real. Attacks cross it exactly as a real adversary would.

---

## Three scenarios

```bash
# Nation-state APT — phishing entry, full station capture
python3 aegis/aegis.py --scenario aegis/scenarios/nation_state_capture.yaml

# Supply chain — malicious PyPI package targeting Vast ground tools
# XZ Utils technique applied to flight software dependency chain
python3 aegis/aegis.py --scenario aegis/scenarios/supply_chain_vendor.yaml

# Insider threat — ground operator with malicious intent
python3 aegis/aegis.py --scenario aegis/scenarios/insider_ground_ops.yaml
```

---

## Countermeasure ranking

AEGIS ranks every identified gap by one metric:

```
priority = chains_blocked × crew_safety_weight
```

Life support failures score 10. Data breaches on research payloads score 3. Security prioritization matches mission prioritization.

| Rank | CM ID | Description | Blocks | Weight |
|------|-------|-------------|--------|--------|
| 1 | CM0034 | SBOM + build provenance verification | Steps 2, 3 | 10 |
| 2 | CM0001 | MFA on ground ops SSO — FIDO2 hardware keys | Step 1 | 9 |
| 3 | CM0019 | Secure boot + code signing on OBC | Step 3 | 10 |
| 4 | CM0041 | Independent sensor validation + physical analog gauges | Step 5 | 10 |
| 5 | CM0007 | Command authentication MAC + replay detection | Steps 4, 6 | 9 |

---

## Project structure

```
.
├── aegis/                          Tier 1 — AEGIS core
│   ├── aegis.py                    Main entrypoint
│   ├── scenarios/                  Attack scenario definitions
│   │   ├── nation_state_capture.yaml
│   │   ├── supply_chain_vendor.yaml
│   │   └── insider_ground_ops.yaml
│   ├── sparta/                     SPARTA v3.2 knowledge base
│   ├── planner/                    Claude API — attack chain generation
│   ├── analysis/                   Gap analysis + crew safety scoring
│   ├── defensive/                  OPA, Sigma, Terraform generators
│   ├── outputs/                    Debrief, heatmap, roadmap writers
│   ├── runner/                     Go execution engine
│   ├── lab/                        Haven-1 Docker digital twin
│   └── generated/                  All AEGIS output files
│
├── thevision-tier2/                Tier 2 — The Fleet
│   ├── run_fleet.py                Fleet General demo entrypoint
│   ├── show_decisions.py           Replay General's reasoning log
│   └── fleet/
│       ├── general.py              Fleet General — Claude API reasoning
│       ├── scout.py                Passive recon agent
│       ├── phantom.py              Credential theft agent
│       └── breacher.py             Exploitation agent
│
├── sovereign/                      Tier 3 — SOVEREIGN architecture
│   ├── phantom_reach_poc.py        PHANTOM REACH POC
│   └── docs/                       Architecture documentation
│
└── thevision-tier3/
    └── files/
        ├── SOVEREIGN_ARCHITECTURE.md
        ├── CIPHER_BINARY_SPECIALIST.md
        ├── GUARDIAN_DEFENSIVE_GUARDIAN.md
        └── PHANTOM_REACH_STEALTH_ARCHITECT.md
```

---

## Compliance coverage

| Framework | Coverage |
|-----------|----------|
| SPARTA v3.2 | Native — all TTPs and countermeasures use SPARTA identifiers |
| NIST SP 800-53 Rev 5 | Full CM-to-control mapping across all 23 identified gaps |
| NIST IR 8401 | Ground segment satellite cybersecurity alignment |
| SPD-5 | Commercial space cybersecurity principles |
| IEC 62443 | OT zone model for life support network isolation |
| CISA Space Systems Guidance | Threat-informed design alignment |

---

## SOVEREIGN — the vision

```
A space station that is SOVEREIGN defends itself autonomously.
Detects threats without ground intervention.
Patches vulnerabilities in orbit.
Cannot be captured, controlled, or coerced by any adversary.

Vast's mission is continuous human presence in space
for America and its allies.

A SOVEREIGN space station is one that cannot be taken from them.
```

Four capabilities. No ground intervention required.

- **Autonomous threat detection** — Sentinel and Oracle monitor all station systems. Anomaly detection tuned to exact attack behaviors THE FLEET discovered. No ground team needed to trigger an alert.
- **In-orbit patch deployment** — Medic generates patches from live findings. Forge signs with station-trusted keys. Hot-deployed to running RTOS without a reboot or ground window.
- **Autonomous incident response** — Warden executes pre-authorized response playbooks. Crew safety constraints formally specified and cannot be overridden. Ground is notified, not consulted.
- **Continuous compliance posture** — Judge documents every detection, response, and patch event against CMMC 2.0, NIST 800-171, and ITAR in real time. Audit-ready at any moment.

---

## Prerequisites

```bash
# Python dependencies
pip install anthropic networkx pyyaml rich pymodbus

# Go execution runner
go install ./aegis/runner/cmd/runner

# Policy tooling (macOS)
brew install opa conftest

# Environment
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Disclaimer

All techniques are derived from publicly available SPARTA v3.2 documentation. All simulations execute exclusively against isolated Docker lab environments. No production systems, no real spacecraft, no operational infrastructure involved.

```
Framework:  SPARTA v3.2 — The Aerospace Corporation
Compliance: NIST SP 800-53 Rev 5 · NIST IR 8401 · IEC 62443
Reference:  SPD-5 · CISA Space Systems Guidance 2024
```

---

## Author

Jordan Rodgers · [jordanrodgers.dev](https://jordanrodgers.dev) · [github.com/jolly-rodgers](https://github.com/jolly-rodgers)
