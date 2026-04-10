# Interview Q&A — Preparation Document
## Jordan Rodgers — Vast Space Staff Offensive Security Engineer

---

## Questions You Will Be Asked

---

### "Walk me through AEGIS."

*"AEGIS is an autonomous adversary simulation platform
built specifically for Haven-1.*

*It starts by generating an AI attack chain — Claude
reasons over the SPARTA knowledge base and Haven-1's
actual architecture to produce a realistic kill chain.
Not generic. CryptoLib, cFS, Modbus, CCSDS — your
actual stack.*

*The chain executes against an isolated Docker lab
modeling your ground and space segment. 12 steps.
8.5 seconds. 12 of 12 pass.*

*Claude then analyzes every successful step and
identifies the missing countermeasures — 93 gaps
ranked by crew safety impact. One fix — CM0007,
enabling CCSDS encryption — blocks 10 of 12 steps.*

*Then it generates the fixes. OPA policy, Sigma rules,
Terraform. Working code, not a findings list.*

*Let me show you."*

---

### "How does the AI decide which TTPs to use?"

*"Claude receives two things: the SPARTA knowledge base
with 12 Haven-1 specific techniques, and a detailed
architecture context describing Haven-1's actual stack —
the software, the protocols, the CVEs.*

*It reasons about which techniques make sense for this
specific actor against this specific target. If I swap
the target environment the chain changes. If I swap the
threat actor the priority and sequencing changes.*

*It's not selecting from a fixed script. It's reasoning
about Haven-1 specifically. The CryptoLib CVE references,
the Modbus register addresses, the Okta SSO gaps — Claude
produced those because we gave it the architecture context
to reason about."*

---

### "What's different about this vs a standard pen test?"

*"Three things.*

*Speed. A traditional engagement gives you point-in-time
visibility twice a year. AEGIS runs continuously. Every
architecture change gets tested automatically.*

*Completeness. A human red team follows a methodology.
AEGIS reasons over the full SPARTA knowledge base and
selects techniques based on what the architecture
actually exposes. It found 93 gaps across 12 steps.*

*Output. Traditional engagements produce reports that
sit in a backlog. AEGIS produces working code. OPA
policies, Sigma rules, Terraform configs. Deploy the
same day. No translation required."*

---

### "Could a real attacker actually do this?"

*"Every technique maps to a documented SPARTA TTP used
by real threat actors against real space infrastructure.*

*The CryptoLib CVEs — CVE-2025-29912 and CVE-2025-59534
— are real documented heap buffer overflows in the
actual library that handles CCSDS security. They went
undetected for three years.*

*The supply chain technique — XZ-style long-game
contributor infiltration — that's exactly what happened
to XZ utils in 2024. Applied here to cFS.*

*The command replay attack was demonstrated live at
DEF CON against spacecraft simulators.*

*The sensor spoofing is the Stuxnet technique applied
to life support instead of centrifuges. Same concept.
Higher stakes."*

---

### "Why Haven-1 specifically?"

*"Because specificity is what makes this real.*

*Anyone can build a generic spacecraft security tool.
AEGIS targets cFS, CryptoLib, CCSDS, Modbus — the
actual stack Haven-1 runs.*

*Seven of your leadership team came from SpaceX.
That tells me the architecture heritage. CryptoLib
handles your CCSDS security. That tells me the attack
surface. The CVEs are documented. That tells me the
specific vulnerability.*

*I built the threat model against your actual
architecture, not a generic spacecraft. That's the
difference between a tool and a platform."*

---

### "What would you build next?"

*"Three things in 90 days.*

*First — close the Fleet feedback loop. Right now the
chain is generated upfront and executed linearly. The
next phase is an adaptive agent that reads each step
result and selects the next technique dynamically.
If one path is blocked it reasons about why and finds
another. That's how real APTs operate.*

*Second — directed fuzzing against cFS. Point AFL++
with angr-informed seed generation at the CryptoLib
TC frame parser. Turn the simulated CVE into a
demonstrated exploit. Prove the vulnerability is real,
not just referenced.*

*Third — the GUARDIAN prototype. Physics-based anomaly
detection on the OBC container. Show that sensor
spoofing is detectable when you model what the physics
says should be happening versus what telemetry reports.*

*Together those three things are SOVEREIGN — the three-
year vision. I'm happy to walk through the full
architecture."*

---

### "How does the Fleet differ from AEGIS?"

*"AEGIS thinks like one analyst with a very good
knowledge base.*

*The Fleet thinks like an APT group — specialists who
never know what the others are doing, coordinated by
a General who reasons about the mission in real time.*

*The key difference is adaptation. AEGIS generates a
plan then executes it linearly. The Fleet General
observes each result and reasons about the next move.
If Breacher is blocked the General doesn't retry the
same path — it reasons about why, queries the SPARTA
knowledge base for alternatives, and tasks a different
agent with a different approach.*

*That's not scripted. That's the AI reasoning about
Haven-1 in real time.*

*I can show you the General's actual decisions from
the last run. Watch crew safety impact escalate from
none to low to high to critical as the kill chain
progresses. The General understood the stakes
without being told."*

---

### "What does CIPHER actually do? Does it use AI?"

*"CIPHER does not use AI to find vulnerabilities.
It uses mathematics.*

*AFL++ is a coverage-guided fuzzer — it mutates inputs
and measures which code paths were hit. Pure math.
50,000 executions per second on an M4 Mac.*

*angr builds a control flow graph of the binary and
identifies which inputs reach dangerous code paths.
Pure static analysis.*

*Z3 is Microsoft's theorem prover. A ROP chain is a
constraint satisfaction problem — find a gadget sequence
such that the instruction pointer equals the shellcode
address and the stack is aligned. Z3 solves that the
same way it solves any constraint system.*

*No training. No model. Mathematical proof.*

*The human provides target selection, the fuzzing
harness, and architectural weakness insight — the
things only a human can do. CIPHER provides scale —
the things only a machine can do. Together we cover
the full attack surface."*

---

### "What's the business case?"

*"A breach on Haven-1 costs an estimated two billion
dollars. Crew rescue, vehicle loss, legal liability,
reputational damage, regulatory response.*

*AEGIS costs 532 thousand dollars in year one.*

*That is a 3,700 times return on the first incident alone.*

*More importantly — and this is the number that matters
most — four crew members cannot wait eight minutes for
ground to respond to an attack. Eight minutes is the
signal delay. GUARDIAN responds in ninety seconds.
Autonomously. Without a reboot.*

*That capability does not exist anywhere else.*

*The question isn't whether Vast can afford AEGIS.
The question is whether Vast can afford not to have it."*

---

### "What certifications do you have / are pursuing?"

*"My background gives me the technical foundation
across exploitation, binary analysis, and red team
operations.*

*For this role specifically I'm focused on depth over
breadth. CRTO for red team operational tradecraft —
it maps directly to the kill chain methodology in AEGIS.
OSED for exploit development depth — needed to defend
CIPHER's ROP chain construction credibly. GREM for
binary analysis — the foundation CIPHER is built on.*

*But the honest answer is that AEGIS demonstrates more
than any certification would. A cert proves you completed
a course. AEGIS proves I can build a working adversary
simulation platform against your specific architecture
in two weeks."*

---

### "What's your three-year vision for Vast's security?"

*"SOVEREIGN.*

*Year one: AEGIS fully deployed against real Haven-1
architecture. The Fleet adaptive loop operational.
Mission risk score updated continuously. Weekly
automated red team reports to engineering leadership.*

*Year two: CIPHER operational. First zero-day discovery
in cFS. PHANTOM REACH demonstrates the full stealth
pivot. GUARDIAN prototype deployed — first autonomous
hot-patch in orbit.*

*Year three: Full SOVEREIGN integration running
continuously against Haven-2's digital twin. Every
new module tested automatically on integration.
Security is a design input to Haven-2, not an
afterthought.*

*By the time forty people are living permanently on
the Artificial Gravity Station, the security
infrastructure protecting them should already exist.*

*SOVEREIGN is that infrastructure.*
*It starts with AEGIS.*
*It starts today."*

---

## Things to Never Say

```
"Hopefully this works..."     You tested it. It works.
"This is just a simulation"   It's a purpose-built lab.
"I'm not sure but..."         If unsure, say you'll find out.
"Sorry, let me..."            Never apologize during a demo.
"As you can see..."           They can see. Don't narrate obvious.
```

## Things to Always Say

```
"Haven-1 specific"            Not generic. Their actual stack.
"Crew safety"                 This is the metric that matters.
"Working code"                Not a report. Deployable output.
"Continuous"                  Not point-in-time. Always running.
"Scales with the program"     Haven-1 today. Haven-2 tomorrow.
"Mathematical proof"          Not a scan result. A proof.
```

---

## Timing Guide

```
Business demo only           4 minutes
AEGIS live demo              6 minutes
Fleet demo                   3 minutes
PHANTOM REACH POC            5 minutes
Full technical walkthrough   25 minutes
Q&A                          15 minutes
```
