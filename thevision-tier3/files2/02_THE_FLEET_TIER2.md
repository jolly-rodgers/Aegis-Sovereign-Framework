# THE FLEET — Tier 2
## Autonomous Multi-Agent Adversary Simulation System

---

## What It Is

An AI agent fleet where a reasoning General orchestrates
14 specialized attack and defense agents against Haven-1's
digital twin. Each agent is an expert in one domain.
They work in parallel. They adapt in real time.
Attack and defense run simultaneously.

This is how real nation-state APT groups operate.
The Fleet models that structure.

---

## Why a Fleet Beats a Single Agent

```
Single agent problems:
  Context window fills on complex operations
  One failure stops the entire operation
  Cannot parallelize reconnaissance
  Cannot run attack and defense simultaneously
  Cannot specialize deeply in any domain

Fleet advantages:
  Each agent expert in one domain
  Agents run in parallel
  One failure does not stop the mission
  Attack fleet and defense fleet run together
  General coordinates without doing the work
  Exactly how real APT groups are structured
```

---

## The Fleet General

The only agent that sees the full picture.

```
Does NOT execute attacks directly.
Does NOT write fixes directly.
DOES reason about mission objectives.
DOES map findings to SPARTA v3.2.
DOES assign tasks to specialist agents.
DOES adapt strategy when agents are blocked.
DOES maintain crew safety as primary metric.

Technical implementation:
  Claude API as the reasoning engine
  SPARTA v3.2 as the knowledge base
  MITRE ATLAS for AI-specific techniques
  Every decision logged with reasoning chain
```

---

## The 14 Agents

```
ATTACK FLEET
  Scout     Passive recon — no writes, no auth, no noise
  Phantom   Identity and credential specialist
  Breacher  Exploitation specialist
  Wraith    Persistence and stealth
  Courier   Intelligence exfiltration
  Hammer    Active phase execution

INTEL FLEET
  Mapper    Architecture graph maintenance
  Analyst   Vulnerability intelligence
  Oracle    Predictive threat intelligence

DEFENSE FLEET
  Medic     Autonomous remediation
  Forge     Secure build and signing
  Sentinel  Continuous detection
  Warden    Incident response
  Judge     Compliance documentation
```

---

## Agents Currently Built (POC)

```
Fleet General   Live Claude API reasoning     BUILT
Scout           Passive recon                 BUILT
Phantom         Credential theft              BUILT
Breacher        CVE-2025-29912 exploitation   BUILT

Remaining 10 agents:                         ROADMAP
```

---

## What the General Actually Reasoned
### From live demo run — not scripted

```
Decision 1 — After mission brief:
  "Initialize nation-state APT campaign with
   phased approach prioritizing intelligence
   gathering before active exploitation."
  SPARTA: TA0043 Reconnaissance
  Crew: none

Decision 2 — After Scout report:
  "Dual-path attack strategy.
   Primary: IA-0007 ground identity (MFA gaps).
   Secondary: EX-0009 CryptoLib fallback."
  SPARTA: IA-0007 → EX-0009
  Crew: low

Decision 3 — After Phantom report:
  "Advance to execution via supply chain.
   Task Breacher to exploit CVE-2025-29912
   using captured CI/CD signing key."
  SPARTA: EX-0009 → IA-0005.01 → PER-0003
  Crew: HIGH

Decision 4 — After Breacher report:
  "CRITICAL MILESTONE. Implant confirmed.
   Task Wraith for telemetry normalization.
   Courier on standby. Hammer on standby.
   Strict operational boundaries to prevent
   crew safety incidents."
  SPARTA: EX-0009 → PER-0003 → DE-0003
  Crew: HIGH
```

Notice crew safety escalating as the kill chain
progresses. The General understands the stakes.
This reasoning was not scripted.

---

## How the General Adapts

```
If Breacher is blocked by signature check:

  General observes: "Update rejected"
  General reasons:  "Signature check failed.
                     What signs artifacts?
                     Jenkins signing key.
                     Phantom has CI/CD access.
                     Task Phantom to extract key."
  General tasks:    Phantom — extract signing key
  Result:           Alternative path found

This is genuine adversarial reasoning.
Not rule-based. Not scripted.
The agent finds paths the human analyst
did not think to model.
```

---

## Fleet Communication Protocol

Every message between agents contains:

```json
{
  "from":       "SCOUT",
  "to":         "GENERAL",
  "type":       "REPORT",
  "payload":    { "finding": "...", "evidence": "..." },
  "reasoning":  "Why this message was sent",
  "confidence": 0.94,
  "timestamp":  "2026-04-07T20:30:30"
}
```

Full audit trail of every decision.
Every reasoning chain logged.
Complete forensic record of the operation.

---

## AEGIS vs The Fleet

```
AEGIS (Tier 1)              THE FLEET (Tier 2)
────────────────────────────────────────────────
Single AI generates chain   AI fleet reasons together
Linear execution            Adaptive — pivots when blocked
Sequential steps            Parallel agent operation
Plan then execute           Reason and execute together
Point-in-time               Continuous
Human reviews output        Defense activates automatically
```

---

## Demo Command

```bash
# Demo mode — no Docker, live Claude API
cd /path/to/thevision-tier2
python3 run_fleet.py --demo

# Live mode — Docker required
python3 run_fleet.py

# Show General's reasoning after run
cat generated/fleet_log.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for i, d in enumerate(data['decisions'], 1):
    dec = d['decision']
    print(f'Decision {i}: {d[\"situation\"]}')
    print(f'  Action: {dec.get(\"decision\", \"\")}')
    print(f'  SPARTA: {dec.get(\"sparta_mapping\", \"\")}')
    print(f'  Crew:   {dec.get(\"crew_safety_impact\", \"\")}')
    print()
"
```

---

## What to Say During the Demo

*"Watch the General's reasoning. After Scout reports
the attack surface, it doesn't just move to the next step —
it reasons about two parallel attack paths and picks the
one with highest confidence.*

*After Phantom reports the signing key, crew safety impact
jumps from low to high. The General understands that signing
capability means OBC compromise is now possible.*

*After Breacher confirms the implant, the General immediately
tasks Wraith for telemetry normalization — unprompted —
because it knows that is the next operational requirement.*

*That is not scripted. That is the AI reasoning about
Haven-1 specifically."*
