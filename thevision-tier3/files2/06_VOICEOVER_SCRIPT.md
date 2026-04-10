# Demo Voiceover Script
## Jordan Rodgers — Vast Space Interview

---

## Setup Checklist (Before Demo)

```
□ Terminal open, font size 18+, dark theme
□ Docker Desktop running
□ Lab containers started (docker compose up -d)
□ ANTHROPIC_API_KEY exported
□ Browser open to last heatmap run
□ demo_business.py ready to run
□ run_fleet.py ready to run
□ phantom_reach_poc.py ready to run
□ Mic on, background quiet
□ Phone on silent
□ Second monitor for notes (if available)
```

---

## Script 1 — Business Demo (4 minutes)
### Use first, regardless of audience

---

**[Terminal open. demo_business.py visible but not running.]**

"Before I show you the live system I want to frame
why this exists — because the engineering is only
half the story.

Haven-1 is the first crewed commercial space station.
Four people. In orbit. Dependent on software for
every life-critical system.

The question I started with wasn't
'can this be hacked' — the answer is always yes.
The question was 'what does it cost when it is'
and 'what does it cost to prevent it.'

Let me show you what I found."

**[Run: python3 demo_business.py]**

**[As attack chain animates — read steps calmly:]**

"Supply chain. Ground system. Persistence.
Reconnaissance. Exfiltration. Sensor spoofing.
Telemetry obfuscation. Command replay.
RF exfiltration. Station capture.

Twelve steps. Zero failures.
Four crew with O2 at 14.2 percent.
Ground ops completely blind.
Station under adversary control."

**[As breach costs render:]**

"These numbers come from IBM's Cost of a Data Breach
report, Lloyd's space insurance data, and Space ISAC
incident records.

Crew rescue operation — 180 million.
Vehicle loss — 400 million.
Legal liability for crew harm — 350 million.

Total expected breach cost: north of two billion dollars.

That is not a security problem.
That is an existential business problem."

**[As headcount section renders:]**

"The traditional answer to this is headcount.
Four L1 analysts doing alert triage.
Two L2 analysts for incident response.
Two external red team engagements per year.

That model costs two and a half million annually
and gives you point-in-time visibility twice a year.

AEGIS gives you continuous visibility
for a fraction of that cost."

**[As ROI section renders:]**

"Year one — 532 thousand dollars.
Year two and beyond — 352 thousand.

Against a two-billion-dollar breach scenario
that is a 3,900 times return on the first incident alone.

The question is not whether Vast can afford AEGIS.
The question is whether Vast can afford not to have it."

**[Pause. Let the closing render. Let it land.]**

---

## Script 2 — AEGIS Live Demo (6 minutes)
### After business demo

---

**[Reset lab: docker compose down && docker compose up -d && sleep 8]**

"Let me show you AEGIS running end to end.
Everything you're about to see is live —
real AI calls, real Docker containers,
real attack steps against a simulated Haven-1."

**[Run: python3 aegis.py]**

**[As lab check runs:]**

"Six Docker containers across two network segments.
Ground — identity provider, CI/CD, ground station.
Space — onboard computer, life support OT, comms.

The network boundary between them is real.
The attack has to cross it. Just like the real thing."

**[As chain generates — read each step as it appears:]**

"Supply chain compromise — 18-month CryptoLib
contributor infiltration. CVE-2025-29912.
Real documented vulnerability in the library
that handles CCSDS authentication for Haven-1.

Ground system — engineer phished. Okta token captured.
No MFA enforcement. That is the gap.

Persistence — refresh tokens harvested.
Password reset will not remove this access.

Jenkins pipeline backdoored. Every future build
re-implants the OBC. Vast cannot patch their way
out of this without fixing the build system first.

Implant installed. Persistent foothold.
Survives reboot.

Reconnaissance — 19 commands intercepted.
Passive. No alerts. Full control language mapped.

Exfiltration — command intelligence encoded
steganographically in housekeeping telemetry.
Ground sees normal data. Attacker C2 has the playbook.

Sensor spoofing — O2 reported 20.9 percent.
Actual 14.2. Hypoxia threshold is 16.
Crew is in danger. Ground sees nominal.

Telemetry obfuscation — everything ground sees is false.
Station looks healthy.

Command replay — propulsion sequences replayed.
CVE-2025-29912 bypasses the replay counter.
Station maneuvers. Comms cut simultaneously.

RF exfiltration — real-time status to foreign asset
during approach.

Station capture — hatch opened via implant.
Four crew. O2 at 14.2. No comms with Vast.
Haven-1 is under adversary control."

**[As gap analysis runs:]**

"Claude is analyzing each step individually.
For every technique that succeeded it identifies
which countermeasures were absent, maps to NIST,
scores by crew safety impact."

**[As gap analysis completes:]**

"93 gaps across 12 steps.

Top fix — CM0007 — CCSDS encryption.
Haven-1's uplink authenticates but does not encrypt.
Every command travels in cleartext.

Enable AES-256-GCM in CryptoLib.
That one fix blocks 10 of 12 attack steps.

That is the finding that matters.
Not 93 vulnerabilities.
One fix that collapses the kill chain."

**[As heatmap opens:]**

"Every red cell is a technique that succeeded.
Scroll down — every one has the specific fix.
How the attack worked against Haven-1 specifically
and the deployable remediation code."

**[Run OPA demo:]**

"Now watch one of those fixes deployed live."

**[As conftest runs on compromised artifact:]**

"Six failures. SBOM required. CryptoLib 1.4.0 vulnerable.
Build provenance missing. Wrong signing account.

This policy was auto-generated by AEGIS.
Not written manually. Generated from the gap analysis.
Deployed in under five minutes."

**[As conftest runs on patched artifact:]**

"Six passes.

The supply chain attack that started the entire
kill chain is now blocked at the CI/CD gate.
Before it reaches the OBC.
Before it reaches the crew."

**[Pause.]**

"That is AEGIS. Found the attack path.
Identified every gap. Generated the fix.
Verified the fix works.
In under 10 minutes."

---

## Script 3 — The Fleet Demo (3 minutes)
### After AEGIS

---

**[Run: python3 run_fleet.py --demo]**

"AEGIS thinks like one analyst.
The Fleet thinks like an APT group —
specialists who never know what the others are doing,
coordinated by a General who reasons about the
mission in real time.

The General is making live Claude API calls right now.
Watch."

**[As Scout runs:]**

"Scout is mapping the attack surface.
Passive only. No packets sent. No authentication.
Pure observation.

CVE-2025-29912 confirmed in stack.
Auth gaps documented.
Command vocabulary mapped.
All without alerting a single monitoring system."

**[As Phantom runs:]**

"Phantom is targeting the highest-clearance engineer.
Token captured. MFA — not required. Gap confirmed.
Signing key extracted from CI/CD environment.
Any artifact signed with this key will be trusted
by Haven-1's OBC."

**[As Breacher runs:]**

"Breacher has the signing key.
Malicious cFS update constructed.
Signed with the legitimate key.
OBC receives, validates, installs.
Implant active."

**[Show General's decisions:]**

"This is what the General reasoned.

After Scout: dual-path strategy, MFA gap as primary.
After Phantom: advance to exploitation via supply chain.
After Breacher: critical milestone. Task Wraith.
Prepare Courier. Hammer on standby.

Watch crew safety escalate — none, low, high, critical.
The General understood the stakes without being told.
This was not scripted."

---

## Script 4 — PHANTOM REACH POC (5 minutes)
### SOVEREIGN demonstration

---

**[Run: python3 phantom_reach_poc.py --demo]**

"This is SOVEREIGN — the three-year vision.
PHANTOM REACH is the stealth component.

Watch both columns.
Left is what is actually happening.
Right is what Haven-1 telemetry shows."

**[Phase 1:]**

"Phase one. Ground portal.
SQL injection in the telemetry query API.
Code execution on the web server.
Valid credentials captured.

Right column: no anomalous authentication events."

**[Phase 2:]**

"Phase two. Lateral movement.
SOCKS proxy over port 443.
Traffic looks like HTTPS.
Optical terminal management network identified.

Right column: no network alerts."

**[Phase 3:]**

"Phase three. Optical link crossing.
Starlink terminal management interface.
Default credentials.
Space-facing interface reachable.
Traffic disguised as data relay.

Right column: link utilization normal range."

**[Phase 4:]**

"Phase four. Life support network.
Modbus TCP. No authentication. By design.
O2 register written. Falsified to 20.9 percent.
Actual: 14.2 percent. Dropping.
Crew has 47 minutes before incapacitation.

Right column: all systems nominal."

**[Phase 5 — stealth validation:]**

"Side by side.
Full attack in progress.
Crew at risk.
Station compromised.

Right column: zero anomalies.
Zero alerts.
Zero indication anything is wrong.

This attack is completely invisible
to standard telemetry monitoring.

This is why GUARDIAN uses physics-based
anomaly detection instead of signatures.

The physics model predicts what O2 SHOULD be
given four crew, given the generation rate,
given the consumption rate.
Any reported value that violates physics
is flagged immediately.

The attacker can spoof the reported value.
They cannot spoof the laws of thermodynamics."

---

## Closing — The Three-Year Vision

"AEGIS is what I built to show you how I think.
The Fleet is what I would build in the first year.
SOVEREIGN is why you keep me.

By the time forty people are living permanently
in space on the Artificial Gravity Station,
the threat actors targeting them will have had
a decade to study the architecture.

SOVEREIGN gives Vast a decade head start.

That is the work I want to do.
That is the mission I came here for."

---

## Energy and Pacing Notes

```
Speak slower than feels natural
Let terminal output breathe — don't talk over it
Never apologize or say "hopefully"
When O2 hits 14.2% — pause. Let it land.
When GUARDIAN patches in 90 seconds — pause.
The silence is part of the demo.

You built this. You understand every line.
Calm confidence. Not excitement.
This is the work. Show it.
```
