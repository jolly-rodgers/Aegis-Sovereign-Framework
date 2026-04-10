# SOVEREIGN — Presentation Slide Notes
## Interview and Pitch Reference Document

---

## Slide 1 — Title

**SOVEREIGN**
Space Operations Vehicle for Emergent Resilience,
Exploitation, Intelligence, and Galactic Network Defense

*The three-year security vision for Haven-1,
Haven-2, and the Artificial Gravity Station.*

**What you say:**
"SOVEREIGN is not a product. It is a program.
A multi-year security architecture that grows
with Vast's mission from Haven-1 through permanent
human presence in space.

I'll show you where it starts — today —
and where it ends up in 2029."

---

## Slide 2 — The Three Tiers

```
TIER 1    AEGIS         Built. Runs today.
          AI-driven SPARTA emulation
          12-step kill chain. 93 gaps. 8.5 seconds.

TIER 2    THE FLEET     POC built. Runs today.
          Autonomous multi-agent orchestration
          General + Scout + Phantom + Breacher

TIER 3    SOVEREIGN     Vision. 3-year build.
          Full autonomous attack and defense
          CIPHER + Fleet + PHANTOM REACH + GUARDIAN
```

**What you say:**
"AEGIS gets you in the door.
The Fleet is what you build in the first year.
SOVEREIGN is why you keep me."

---

## Slide 3 — CIPHER (Binary Specialist)

**The one sentence:**
A custom CCSDS protocol fuzzer that discovers
real zero-days in flight control binaries and
proves exploitability via Z3 constraint solving —
not CVE references, working exploits.

**Key technical points:**
- AFL++ with angr-directed seed generation
- Targets CryptoLib TC frame authentication
- Z3 SMT solver constructs ROP chain mathematically
- Manticore symbolic execution validates the chain
- Output: mathematical proof of code execution

**The demo moment:**
Show the Z3 solver output — the gadget sequence
with the satisfiability certificate.
"Z3 proved this chain achieves code execution.
This is not a scan result. This is a proof."

**What it feeds to The Fleet:**
Working shellcode. Real payload. Not CVE ID.
Breacher agent has actual exploit capability.

---

## Slide 4 — THE FLEET (Fleet General)

**The one sentence:**
An AI agent fleet where a reasoning General
orchestrates 14 specialized attack and defense agents
against Haven-1 — adapting in real time based on
what each agent discovers.

**Key technical points:**
- Claude API as the reasoning engine
- SPARTA v3.2 as the knowledge base
- 14 agents: 6 attack, 3 intel, 5 defense
- General adapts when agents are blocked
- Attack and defense run simultaneously

**The demo moment:**
Show the General's actual decisions from the log.
"This reasoning was not scripted.
Claude reasoned about Haven-1 specifically.
Watch crew safety impact escalate as
the kill chain progresses."

**What makes it different from AEGIS:**
AEGIS generates a plan then executes linearly.
The Fleet reasons, adapts, and pivots.
Real APTs adapt. The Fleet models that.

---

## Slide 5 — PHANTOM REACH (Stealth Architect)

**The one sentence:**
A complete undetected pivot from Haven-1's
internet-facing ground portal through the
optical link to the internal life support
network — generating zero anomalous signatures
in standard telemetry monitoring.

**Key technical points:**
- OSWE: white-box web exploitation on ground portal
- OSEP: C2 over allowed protocols, traffic blending
- Optical terminal compromise — embedded Linux
- Modbus TCP has no authentication
- Side-by-side: attack timeline vs telemetry

**The demo moment:**
Side-by-side screen:
Left: full attack in progress
Right: Haven-1 telemetry showing all normal
"This attack is completely invisible."

**Why this matters:**
Proves that standard monitoring is insufficient.
Validates the need for GUARDIAN's physics-based
anomaly detection rather than signature detection.

---

## Slide 6 — GUARDIAN (Defensive Guardian)

**The one sentence:**
An AI-driven EDR built specifically for Haven-1's
RTOS that detects the exact memory corruption
CIPHER discovered and hot-patches the binary
in orbit in under 90 seconds — no reboot,
no crew disruption, no ground intervention.

**Key technical points:**
- Physics-based anomaly detection (not signatures)
- CIPHER signatures integrated at build time
- Binary lift to LLVM IR for patch synthesis
- HSM-signed patch deployment
- Human approval gate for flight-critical systems
- Full forensic preservation before any response

**The demo moment:**
Timer on screen counting seconds.
"Detection: 0.5 seconds.
Containment: 2 seconds.
Patch synthesized: 30 seconds.
Patch deployed: 60 seconds.
Exploit re-run: blocked.
No reboot. Crew never knew."

**The key differentiator:**
Standard EDR reboots to patch.
Haven-1 cannot reboot.
GUARDIAN hot-patches.
That capability does not exist anywhere else.

---

## Slide 7 — Integration

**The full loop:**

```
CIPHER finds zero-day
  ↓
Fleet General receives proof
reasons about SPARTA impact
tasks agents with real payload
  ↓
Attack Fleet executes          Defense Fleet activates
Scout → Phantom →              Medic generates patch
Breacher(real exploit) →       Sentinel detects behavior
Wraith → Courier → Hammer      GUARDIAN hot-patches
  ↓                              ↓
PHANTOM REACH validates stealth  Patch deployed in 90s
Standard monitoring sees nothing No reboot. No disruption.
  ↓                              ↓
         SOVEREIGN closes the loop
         Attack proven. Defense validated.
         Both simultaneously. Continuously.
```

**What you say:**
"Every component talks to every other component.
CIPHER makes The Fleet real instead of simulated.
PHANTOM REACH proves the defense is necessary.
GUARDIAN proves the defense works.
The loop is complete. Autonomous. Continuous."

---

## Slide 8 — The Timeline

```
Today        AEGIS + Fleet POC
             You can see it running right now

Year 1       Close the Fleet feedback loop
             First directed fuzzing against cFS
             Mission risk score dashboard live

Year 1-2     CIPHER v1 operational
             First crash findings on CryptoLib
             First mathematical exploit proof

Year 2       PHANTOM REACH demonstrated
             Full pivot path proven
             Zero telemetry signature confirmed

Year 2-3     GUARDIAN prototype
             RTOS memory detection
             First autonomous hot-patch

Year 3       SOVEREIGN integrated
             All four components connected
             Running against Haven-2 twin

Year 3+      Industry contribution
             DEF CON Space Village
             SPARTA framework update
             NIST IR 8401 revision input
```

---

## Slide 9 — Why This Matters Beyond Haven-1

**What you say:**

"Haven-1 carries four crew.
Haven-2 will carry eight.
The Artificial Gravity Station will carry
forty people permanently.

The cost of getting security wrong
scales with every person we put in space.
The cost of SOVEREIGN does not.

By the time we have forty permanent residents
in orbit, the threat actors targeting them
will have had a decade to study the architecture.
SOVEREIGN gives Vast a decade head start.

And when the first human is born in space —
whenever that happens — the security infrastructure
protecting them should already exist.

SOVEREIGN is that infrastructure.
It starts with AEGIS.
It ends with humanity living safely
beyond Earth."

---

## Slide 10 — The Ask

**What you say:**

"I built AEGIS to show you how I think.
I built The Fleet to show you what year one looks like.
SOVEREIGN is the three-year vision.

What I want to do is build it here.
With your architecture. Against your real systems.
For your crew.

That is the work I came to do."

---

## Key Questions You Will Be Asked

**"How is this different from a standard pen test?"**
A pen test gives you findings twice a year.
SOVEREIGN runs continuously.
Every architecture change gets tested automatically.
And it fixes what it finds.

**"Can this actually be built?"**
AEGIS exists — you saw it run.
The Fleet exists — you saw it run.
CIPHER uses open-source AIxCC components.
GUARDIAN uses established binary analysis tooling.
The components exist. The integration is the work.

**"What's the crew safety story?"**
Every decision SOVEREIGN makes is weighted by
crew safety impact. The physics model in GUARDIAN
catches threats before crew symptoms appear.
The hot-patch deploys before ground contact is possible.
The crew is protected autonomously because
8-minute signal delay means ground response
is always too slow.

**"How does it scale to Haven-2?"**
New module equals new scenario automatically.
The digital twin updates on every architecture change.
SOVEREIGN scales with the program by design.
Not by retrofit.
