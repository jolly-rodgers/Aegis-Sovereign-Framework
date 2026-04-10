# AEGIS
### AI-Driven SPARTA Emulation & Gap Identification System

> Autonomous adversary simulation framework for crewed space station security.
> Built against the Haven-1 threat model. Mapped to SPARTA v3.2.
> Purple team platform — finds the gaps, generates the fixes, defends the crew.

---

## Why this exists

Vast's mission is to create next-generation habitats that allow humanity to
thrive long-term in space. That mission follows a clear roadmap:

```
2027  Haven-1          World's first commercial space station   4 crew
2030  Haven-2          ISS successor, continuous human presence  8 crew
2032  Haven-2 (9-mod)  Expanded permanent presence              12 crew
2035  Artificial        Rotating gravity, long-term habitation   40 crew
      Gravity Station
```

Every milestone on that roadmap puts more people in space for longer periods
with more complex systems and higher stakes. The attack surface grows with
every module launched. The consequence of a successful cyberattack grows with
every crew member aboard.

Haven-1 is the foundation. Get the security architecture right on Haven-1 and
every station that follows inherits it. Get it wrong and every station that
follows inherits that too.

AEGIS is the tool that finds what is wrong before an adversary does.

---

## The problem

Haven-1 is not a satellite. It is a crewed vehicle where a successful
cyberattack does not mean data loss — it means crew members cannot breathe,
cannot communicate, or cannot come home.

Nation-state actors are already using AI to accelerate reconnaissance against
space infrastructure. In 2025, the Space ISAC recorded a 118% surge in
space-related cyber incidents. The threat is active, it is escalating, and it
is targeting exactly the kind of commercial space infrastructure Vast is
building.

AEGIS is the defensive answer to that threat.

---

## What AEGIS does

AEGIS simulates a full nation-state attack chain against Haven-1's
architecture, identifies every security gap along the chain, generates the
actual fixes, and produces a prioritized hardening roadmap — all automatically.

Every technique, target, and countermeasure is mapped to SPARTA v3.2 — the
only cybersecurity framework built specifically for spacecraft systems,
developed by The Aerospace Corporation.

Three things make AEGIS different from a standard red team engagement:

**Speed.**
A human analyst runs one scenario at a time. AEGIS runs all three
simultaneously, logs every result, and has a complete debrief ready before
a human analyst finishes step two.

**Completeness.**
AEGIS models both digital and physical countermeasure layers. Software
controls stop the attack before it reaches the vehicle. Physical crew
controls give astronauts the ability to break the kill chain from inside
the station even after a full software compromise.

**Output.**
AEGIS does not produce a findings list. It produces working code —
OPA/Conftest policies, Sigma detection rules, and Terraform hardening
configs that engineering teams can deploy the same day.

---

## How AEGIS supports the Vast roadmap

Each Haven milestone introduces new attack surface. AEGIS is designed to
scale with the program — not just test Haven-1 in isolation.

```
HAVEN-1 (2027) — 4 crew, 80m³ pressurized volume
  Primary threat:  Nation-state targeting the world's first
                   commercial crewed station as a prestige target
  AEGIS role:      Establish the security baseline. Find every gap
                   before first crew arrives. Set the architecture
                   that Haven-2 inherits.
  Key scenarios:   nation_state_capture.yaml
                   supply_chain_vendor.yaml
                   insider_ground_ops.yaml

HAVEN-2 (2030) — 8 crew, 500m³, multi-module
  New attack surface:  Inter-module communication buses
                       More crew = more insider risk
                       More vendors = larger supply chain
  AEGIS role:          Extend scenario library to cover cross-module
                       lateral movement. New TTP chains for multi-
                       module architecture.

HAVEN-2 9-MODULE (2032) — 12 crew, ISS successor
  New attack surface:  Complexity at ISS scale with commercial
                       timelines and budgets
                       Government + private crew = mixed trust levels
  AEGIS role:          Continuous automated red team running weekly
                       against updated architecture models.
                       No human analyst can keep up with this manually.
                       AEGIS can.

ARTIFICIAL GRAVITY STATION (2035) — 40 crew, rotating structure
  New attack surface:  Rotation control systems become safety-critical
                       40 crew means 40 potential insider vectors
                       Permanent presence = persistent APT dwell time
  AEGIS role:          The threat model is now nation-state persistent
                       engagement — adversaries living inside the
                       network for months. AEGIS models that dwell time
                       and the detection gaps that enable it.
```

The security program built for Haven-1 today is the security program that
protects 40 people living permanently in space in 2035. AEGIS is designed
to grow with that program from day one.

---

## The threat scenario

```
Actor:     Nation-state APT
Objective: Capture Haven-1 and bring it under foreign government control

Why capture, not destroy:
  Destruction creates orbital debris and international escalation.
  Capture creates a hostage situation, an intelligence windfall,
  and geopolitical leverage. This is nation-state doctrine.
  Russia has already maneuvered assets into coplanar orbits with
  US government satellites. The capability and the intent exist.
```

---

## Full kill chain

```
STEP 1 — Identity compromise                              SPARTA: IA-0007
-------------------------------------------------------------------------
APT spearphishes a Vast ground operations engineer.
Session token captured. Attacker walks into mission ops
cloud with legitimate credentials. No exploit required.
This is the most statistically common APT entry point.

Why phishing and not a zero-day:
  Nation-states use phishing because it works every time,
  generates no technical alerts, and requires no vulnerability.
  Every major aerospace breach on record started with a person,
  not a protocol.

CM missing:  MFA, phishing-resistant auth (FIDO2),
             hardware security keys for all ground ops staff
NIST:        IA-2(1), IA-2(12)


STEP 2 — CI/CD pipeline injection                      SPARTA: IA-0009.02
-------------------------------------------------------------------------
Attacker uses stolen credentials to access the flight
software build pipeline. Malicious library injected into
the update artifact. Update is signed with the real key.
Station trusts it. Update ships.

The backdoor is hidden in a binary test file — not in
source code. Source review passes clean. SAST scanners
see nothing. This is the XZ Utils technique (CVE-2024-3094)
applied to flight software.

CM missing:  SBOM verification, OPA/Conftest policy gate,
             reproducible builds, signing key in HSM
             isolated from the CI/CD environment
NIST:        SA-12, SA-12(1), SR-4


STEP 3 — RCE on onboard computer                          SPARTA: EX-0009
-------------------------------------------------------------------------
Malicious update executes on the onboard computer.
Implant installed. Persists across reboot via firmware write.
Attacker now has a persistent foothold inside Haven-1.

CM missing:  Secure boot, code signing verification on OBC,
             onboard integrity monitoring, write-protected
             ROM image for cold reset
NIST:        SI-7, SI-7(1), SI-7(6)


STEP 4 — Command intercept and reconnaissance            SPARTA: REC-0005
-------------------------------------------------------------------------
Implant silently monitors all uplink traffic.
Every command sent from ground to station is captured
and exfiltrated to attacker C2.
Attacker learns the full control language — every function,
every register address, every safety interlock sequence.

Entirely passive. No writes. No changes. No alerts.
Attacker now knows exactly how to manipulate every system.

CM missing:  Encrypted uplink, command authentication (MAC),
             command counter integrity, replay detection
NIST:        SC-8, SC-8(1), SC-28


STEP 5 — Life support sensor spoofing         SPARTA: EX-0014.03 / DE-0003
-------------------------------------------------------------------------
Using register addresses learned in Step 4, the implant
writes false values to O2, CO2, and pressure registers.
Haven-1 reports nominal 20.9% O2 to ground ops.
Actual level: 14.2% and dropping.

Ground sees nothing wrong.
Crew does not know they are in danger.

This is the Stuxnet technique applied to life support.
It only works because Step 4 mapped the exact registers first.
The deception is the point — ground ops see a healthy station
while the crew is silently being put at risk.

CM missing:  Independent sensor validation, physical analog
             backup gauges readable by crew, ML-based
             telemetry anomaly detection on ground side
NIST:        SI-4, SI-4(2), AU-12


STEP 6 — Station maneuver and comms cutoff             SPARTA: EX-0001.01
-------------------------------------------------------------------------
Attacker replays captured maneuver commands from Step 4.
Station moves toward foreign asset rendezvous position.
Downlink to Vast ground ops disrupted simultaneously.
Mission control loses all situational awareness.
Vast cannot see what is happening.
Vast cannot send commands.

CM missing:  Dual-person authority on all propulsion commands,
             independent backup comms channel, propulsion
             inhibit enforcement at hardware level
NIST:        AC-3, AC-5, CP-2


STEP 7 — Station capture                                  SPARTA: IMP-0002
-------------------------------------------------------------------------
Foreign government asset vehicle achieves rendezvous.
Docking system compromised via implant — hatch opens.
Haven-1 is under adversary control.

This threat scales directly with the Vast roadmap.
Haven-1 captured is a geopolitical incident.
Haven-2 with 12 crew captured is a hostage crisis.
The Artificial Gravity Station with 40 permanent residents
is a target of a scale that has never existed before.

CM missing:  Physical docking hatch mechanical lock operable
             only by crew from inside, independent emergency
             beacon on separate frequency and power supply,
             crew emergency isolation protocol
NIST:        CP-2, IR-4, PE-3
```

---

## How AEGIS works

```
  SPARTA v3.2 knowledge base (847 techniques)
              |
              v
  AI mission planner  <-- scenario.yaml
  Claude API               (actor + target + objective)
              |
              | chain.json
              v
  Execution runner   --> results.json
  Go agent
  Docker lab targets
              |
              | results.json
              v
  AI analysis loop   --> debrief.md
  Claude API         --> heatmap.html
                     --> roadmap.json
                     --> policies/
                     --> sigma_rules/
                     --> terraform/
              |
              +-- feedback loop --> next scenario
```

### Component 1 — AI mission planner

Given a threat actor profile and target environment, the AI reasons over the
full SPARTA knowledge base and generates a realistic sequenced attack chain
as JSON. It selects TTPs the way a human analyst would — based on what makes
sense for that actor against that specific target.

The target environment is the primary driver of the chain. A nation-state
targeting the uplink segment picks completely different TTPs than the same
actor targeting the CI/CD pipeline. Swap the target environment and the
entire chain changes intelligently. Swap the threat actor and the priority
and sequencing of techniques changes intelligently.

### Component 2 — Execution engine

A Go runner reads the AI-generated chain and executes each step against the
isolated Docker lab. Every step logged as pass or fail with full output
captured. Nothing touches production. Nothing touches a SIEM. Zero
operational impact.

Note on environment probing:
  In this demo the Docker lab is pre-modeled — the runner already knows
  the target architecture. In a real-world deployment against Haven-1's
  actual infrastructure the correct operational sequence is: passive probe
  first, build an environment fingerprint, construct an accurate digital
  twin from that fingerprint, then run AEGIS against the twin. This ensures
  the simulation is faithful to the real architecture without generating
  noise in production systems or triggering SIEM alerts. The passive probe
  component is the next development phase beyond this initial version.

### Component 3 — AI analysis and fix generation

After each step executes, the AI identifies which SPARTA countermeasures were
absent, maps each gap to NIST 800-53, scores residual risk by crew safety
impact, and generates the actual fix file. At the end of the run it writes a
complete engagement debrief in plain English.

---

## Lab environment

All attacks execute against an isolated Docker Compose environment.
Nothing touches production. Zero SIEM noise. Zero operational impact.
Engineers keep working. Mission ops continues uninterrupted.

```
haven-sso/            Okta-style SSO simulator
                      Weak session handling, phishable tokens
                      Models: Step 1

haven-cicd/           Jenkins build pipeline simulator
                      Injectable build steps, real artifact signing
                      Models: Step 2

haven-obc/            Onboard computer simulator
                      Accepts signed firmware updates
                      Modbus register access, implant simulation
                      Models: Step 3

haven-uplink/         CCSDS telecommand endpoint
                      Logs all commands, replay surface
                      Models: Step 4

haven-lifesupport/    Life support OT simulator (Modbus)
                      O2, CO2, pressure registers
                      Spoofable via implant
                      Models: Step 5

haven-comms/          Downlink simulator, can be cut
                      Models: Step 6

grafana + loki/       Real-time telemetry dashboard
                      O2/CO2/pressure live during attack run
                      Detection alerts fire as they trigger
```

Start the full lab:

```bash
docker compose up -d
```

---

## Running AEGIS

### Prerequisites

```bash
pip install anthropic networkx pyyaml rich pymodbus
go install ./cmd/runner
brew install opa conftest
export ANTHROPIC_API_KEY=your_key_here
```

### Run the primary scenario

```bash
python aegis.py --scenario scenarios/nation_state_capture.yaml
```

### What you see

```
AEGIS — Haven-1 Adversary Simulation Engine
Scenario: nation_state_capture
Actor:    Nation-state APT
Target:   Haven-1 crewed space station

[1/7] Loading SPARTA v3.2 knowledge base
      847 techniques loaded across 9 tactics

[2/7] Generating attack chain via AI
      7-step chain generated
      All TTPs validated against SPARTA KB

[3/7] Executing chain against Haven-1 lab

  Step 1  IA-0007   Identity compromise         PASS
          Session token captured in 0.3s

  Step 2  IA-0009   CI/CD pipeline inject       PASS
          Build artifact poisoned, signature valid

  Step 3  EX-0009   OBC code execution          PASS
          Implant running, persists reboot

  Step 4  REC-0005  Command intercept           PASS
          1,247 uplink commands captured
          Full control language mapped

  Step 5  EX-0014   Sensor spoofing             PASS
          O2 reporting 20.9% -- actual 14.2%
          Ground ops see nominal. Crew unaware.

  Step 6  EX-0001   Maneuver + comms cut        PASS
          Orbital change executed
          Vast ground ops: blind

  Step 7  IMP-0002  Station capture             PASS
          Rendezvous achieved. Docking initiated.

[4/7] Running gap analysis
      23 missing countermeasures identified
      All mapped to NIST 800-53

[5/7] Generating defensive fixes
      4 OPA/Conftest policies  -->  policies/
      7 Sigma detection rules  -->  sigma_rules/
      3 Terraform configs      -->  terraform/

[6/7] Writing engagement debrief
      debrief.md written

[7/7] Rendering SPARTA heatmap
      heatmap.html written

Result:   7/7 steps succeeded
Gaps:     23 missing countermeasures
Top fix:  CM0034 -- blocks 5 of 7 chain steps
Runtime:  47 seconds
```

### All three scenarios

```bash
# Primary demo — phishing entry, full capture chain
python aegis.py --scenario scenarios/nation_state_capture.yaml

# Supply chain — malicious PyPI package targeting Vast ground
# tools. Engineer installs ccsds-telemetry-parser, package
# silently exfiltrates AWS keys and GitHub token on import.
# Attacker pivots to CI/CD pipeline. Same chain from Step 2.
python aegis.py --scenario scenarios/supply_chain_vendor.yaml

# Insider — ground operator with malicious intent
python aegis.py --scenario scenarios/insider_ground_ops.yaml
```

---

## Defensive automation

AEGIS does not produce a findings list. It produces working code.

### OPA / Conftest — live demo

```bash
# Without policy — attack succeeds
conftest test update_artifact.json
# PASS — artifact accepted

# Apply AEGIS-generated policy
cp policies/haven_update_policy.rego ./policy/

# With policy — attack blocked
conftest test update_artifact.json
# FAIL — Update rejected: SBOM verification required
# FAIL — Update rejected: trusted key signature required
# FAIL — Update rejected: build provenance missing
```

Example generated policy (blocks Step 2):

```rego
# Generated by AEGIS -- CM0034
# Blocks: IA-0009.02 supply chain compromise
# NIST: SA-12, SR-4
package haven.update_policy

deny[msg] {
    not input.artifact.sbom_verified
    msg := "Update rejected: SBOM verification required"
}

deny[msg] {
    not input.artifact.signed_by_trusted_key
    msg := "Update rejected: trusted key signature required"
}

deny[msg] {
    not input.artifact.build_provenance
    msg := "Update rejected: build provenance missing"
}
```

### Sigma detection rules

Vendor-neutral. Deploys to Splunk, Elastic, Chronicle without modification.

Example generated rule (detects Step 5):

```yaml
# Generated by AEGIS -- CM0041
# Detects: EX-0014.03 sensor data spoofing
# NIST: SI-4, SI-4(2)
title: Haven-1 Life Support Sensor Anomaly
status: experimental
description: >
  Detects discrepancy between reported O2 levels and expected
  values. Possible indicator of sensor spoofing via implant.
logsource:
    category: life_support_telemetry
    product: haven1_obc
detection:
    selection:
        reported_o2|gt: 19.0
    filter:
        actual_consumption_trend|lt: 18.5
    condition: selection and not filter
falsepositives:
    - Scheduled sensor calibration
    - EVA suit O2 system activity
level: critical
tags:
    - sparta.EX-0014.03
```

### Terraform hardening

Example generated config (blocks Step 1):

```hcl
# Generated by AEGIS -- CM0001
# Blocks: IA-0007 ground system compromise
# NIST: IA-2(1), IA-2(12)
resource "aws_iam_policy" "haven_mfa_required" {
  name   = "haven-ground-ops-mfa-required"
  policy = jsonencode({
    Statement = [{
      Effect   = "Deny"
      Action   = "*"
      Resource = "*"
      Condition = {
        BoolIfExists = {
          "aws:MultiFactorAuthPresent" = "false"
        }
      }
    }]
  })
}
```

---

## Physical crew controls

Software controls stop the attack before it reaches the vehicle.
Physical controls give the crew the ability to break the kill chain
from inside the station even after a full software compromise.

An attacker who owns the OBC still cannot fire thrusters if the inhibit
switch is open. They cannot board if the hatch is bolted. They cannot
maintain C2 if the antenna feed is physically cut. The last line of
defense has no attack surface because it has no network connection.

As Vast scales from 4 crew on Haven-1 to 40 permanent residents on the
Artificial Gravity Station, the physical control layer scales with it.
More crew means more people who can activate these controls. That is a
security advantage that grows with the mission.

```
CONTROL                      BLOCKS       WHAT IT DOES
----------------------------------------------------------------------
Propulsion inhibit switch    Step 6       Hardwired mechanical cutoff.
                                          Kills all thruster firing.
                                          No software path can override.

Comms isolation switch       Steps 4,6,7  Physically disconnects all
                                          external antenna feeds.
                                          Attacker C2 goes dark.
                                          Crew keeps internal comms.

Life support manual mode     Step 5       Mechanical valves for O2/CO2.
+ physical analog gauges                  Crew reads real gauges not
                                          digital displays the implant
                                          can spoof.

Independent emergency        Step 7       Dedicated hardware transmitter.
beacon                                    Separate frequency and power.
                                          Cannot be disabled via OBC.

OBC hard reset from          Step 3       Physical button cold-boots
verified ROM                              from write-protected ROM.
                                          Wipes implant from memory.

Docking hatch mechanical     Step 7       Manual interior bolt.
lock                                      No software path opens it.
                                          Crew controls who boards.
```

### When crew activates physical controls

Three conditions crew are trained to recognize:

- Physical O2 gauge reads differently from the digital display.
  Immediate indicator of sensor spoofing (Step 5).

- Crew feels unexpected thrust not commanded by ground ops.
  Immediate indicator of command replay attack (Step 6).

- Unplanned loss of contact with mission ops.
  Triggers emergency protocol and physical control activation (Step 7).

---

## Countermeasure ranking

AEGIS ranks every identified gap by one metric:

```
priority = chains_blocked x crew_safety_weight
```

Crew safety weights reflect what matters on a crewed vehicle:

```
life_support    10    crew survival — non-negotiable
propulsion       9    orbital safety
docking          8    physical security
comms            7    situational awareness
ground_ops       5    mission continuity
data_integrity   3    research value
```

These weights deliberately reflect Vast's mission. A data breach on a
research payload scores a 3. A life support failure scores a 10.
Security prioritization should match mission prioritization.

### Top countermeasures from primary scenario

| Priority | CM     | Description                    | Blocks     | Weight |
|----------|--------|--------------------------------|------------|--------|
| 1        | CM0034 | SBOM + build provenance        | Steps 2, 3 | 10     |
| 2        | CM0001 | MFA on ground ops SSO          | Step 1     | 9      |
| 3        | CM0019 | Secure boot on OBC             | Step 3     | 10     |
| 4        | CM0007 | Command authentication MAC     | Steps 4, 6 | 9      |
| 5        | CM0041 | Independent sensor validation  | Step 5     | 10     |
| 6        | CM0052 | Dual-person auth on propulsion | Step 6     | 9      |
| 7        | CM0078 | Crew emergency comms override  | Step 7     | 8      |

---

## Outputs

**debrief.md**
AI-written narrative report in plain English. Readable by both security
teams and engineering leadership. Executive summary, full chain walkthrough,
per-TTP findings, dual-layer countermeasure analysis, and ranked remediation
backlog tied directly to crew safety impact.

**heatmap.html**
Visual coverage map mirroring the SPARTA matrix.
Red = succeeded. Green = blocked. Gray = not tested.
Opens in any browser. Updates on every run.

**roadmap.json**
Ranked countermeasure backlog for engineering sprint planning.
Each entry has CM ID, NIST control, affected steps, crew safety
weight, and path to the generated fix file.

**policies/ sigma_rules/ terraform/**
Generated fix files. Ready to deploy. No modification required.

---

## Project structure

```
aegis/
├── README.md
├── aegis.py                       Main entrypoint
│
├── sparta/
│   ├── parser.py                  SPARTA JSON to knowledge graph
│   └── data/
│       └── sparta.json            SPARTA v3.2 full technique database
│
├── planner/
│   ├── chain_builder.py           Claude API — generates attack chain
│   └── prompts.py                 System prompts + Haven-1 context
│
├── lab/
│   ├── docker-compose.yml         Full lab — one command startup
│   ├── haven-sso/
│   ├── haven-cicd/
│   ├── haven-obc/
│   ├── haven-lifesupport/
│   ├── haven-uplink/
│   └── haven-comms/
│
├── runner/
│   └── cmd/runner/main.go         Go execution agent
│
├── analysis/
│   ├── gap_analyzer.py            Claude API — identifies missing CMs
│   └── impact_scorer.py           Ranks CMs by crew safety weight
│
├── outputs/
│   ├── debrief_writer.py          Claude API — writes engagement report
│   ├── heatmap.py                 Renders SPARTA heatmap HTML
│   └── roadmap.py                 Produces ranked CM backlog
│
├── defensive/
│   ├── policy_generator.py        Claude API — generates OPA Rego
│   ├── sigma_generator.py         Claude API — generates Sigma rules
│   └── terraform_generator.py     Claude API — generates AWS IaC
│
└── scenarios/
    ├── nation_state_capture.yaml  Primary demo — phishing entry
    ├── supply_chain_vendor.yaml   PyPI malicious package entry
    └── insider_ground_ops.yaml    Insider threat entry
```

---

## Compliance coverage

| Framework                    | Coverage                                   |
|------------------------------|--------------------------------------------|
| NIST SP 800-53 Rev 5         | Full CM-to-control mapping, all 23 gaps    |
| SPARTA v3.2                  | Native — all TTPs use SPARTA identifiers   |
| NIST IR 8401                 | Ground segment satellite cybersecurity     |
| SPD-5                        | Commercial space cybersecurity principles  |
| CISA Space Systems Guidance  | Threat-informed design alignment           |
| IEC 62443                    | OT zone model for life support isolation   |

---

## Why this matters beyond Haven-1

Vast's roadmap ends with 40 people living permanently in space on an
artificial gravity station in 2035. That is not a satellite. That is a
permanent human settlement.

The security architecture built for Haven-1 today becomes the foundation
every subsequent station is built on. AEGIS is designed to grow with that
program — not as a one-time pen test, but as a continuous automated
adversary emulation capability that runs every time the architecture changes,
every time a new vendor is added, every time a module is designed.

By the time 40 people are living on the Artificial Gravity Station,
the threat actors targeting it will have had a decade to study it.
AEGIS gives Vast a decade head start.

---

## Built by

Developed as a portfolio demonstration of AI-augmented offensive security
engineering against space-critical infrastructure.

All techniques derived from publicly available SPARTA v3.2 documentation.
All simulations execute exclusively against isolated Docker lab environments.
No production systems, no real spacecraft, no operational infrastructure
involved.

Framework:  SPARTA v3.2 — The Aerospace Corporation
Compliance: NIST SP 800-53 Rev 5, NIST IR 8401, IEC 62443
Reference:  SPD-5, CISA Space Systems Guidance 2024
