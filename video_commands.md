# VIDEO PRESENTATION — Command Index
## Jordan Rodgers | AEGIS + The Fleet + SOVEREIGN

---

## TIER 1 — AEGIS LIVE (Real Docker Containers)

### Step 1 — Start Docker Desktop
```bash
open -a Docker
```
*Wait 30 seconds for Docker to fully start*

---

### Step 2 — Start the Haven-1 Lab
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab"
docker compose up -d
```
*Wait 8 seconds for all 6 containers to start*

---

### Step 3 — Verify All 6 Containers Are Running
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab"
docker compose ps
```
*Should show 6 containers: ground-identity, ground-pipeline, ground-station, space-obc, space-lifesupport, space-comms — all Running*

---

### Step 4 — Verify Lab Health (Optional — shows detail)
```bash
curl -s http://localhost:8080/health | python3 -m json.tool
curl -s http://localhost:8081/health | python3 -m json.tool
curl -s http://localhost:8082/health | python3 -m json.tool
curl -s http://localhost:8083/health | python3 -m json.tool
curl -s http://localhost:8084/health | python3 -m json.tool
curl -s http://localhost:8085/health | python3 -m json.tool
```
*Each should return status: ok with the correct service name*

---

### Step 5 — Run the Business Case First
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
python3 demo_business.py
```
*~4 minutes. Shows breach cost vs AEGIS cost. No Docker needed for this step.*

---

### Step 6 — Reset Lab to Clean State Before Live Demo
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab"
docker compose down && docker compose up -d && sleep 8
```
*Always reset before a live demo so OBC shows clean (implant_active: false)*

---

### Step 7 — Run Full AEGIS Pipeline (The Main Event)
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
python3 aegis.py
```
*~5-8 minutes total. Runs all 6 stages automatically:*
*1. Lab health check*
*2. AI chain generation (Claude API)*
*3. Go runner — 12 steps against Docker lab*
*4. AI gap analysis (Claude API)*
*5. SPARTA heatmap render*
*6. AI debrief writer (Claude API)*

---

### Step 8 — Open Heatmap in Browser
```bash
open "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/heatmap.html"
```
*Opens interactive SPARTA coverage map. Red = succeeded. Scroll down for remediation detail.*



INSERT THE SPEACH ABOUT THE BUSINESS SIDE AND EXPLAIN WHAT IS HAPPENING ON THE LIVE RUN NOW.
---

### Step 9 — OPA/Conftest Policy Gate Demo
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
bash defensive/opa_demo.sh
```
*Shows: 6 FAIL on compromised artifact. 6 PASS on patched artifact.*
*Key moment: read the REJECTED messages out loud as they appear.*

Show THEM LINKS AND VIDEO OF THE FULL SAND BOX ON MY GITHUB

---

### Step 10 — Show AI-Written Debrief (Optional)
```bash
cat "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/debrief.md"
```
*Full engagement report written by Claude from simulation results.*

SHOW THEM THIS AS AN AUDIT LOG FOR FUTURE PLATFORMS THAT WOULD GENERATE THE OUTP FOR THE PURPLE TEAM SO THEY CAN TROUBLE SHOOT ANYTING THAT WENT WRONG DURING OPERATION.

---

### Step 11 — Show Gap Analysis Summary (Optional)
```bash
THIS IS MORE AUDIT LOGS THAT SHOW WHAT WAS SUCESSFULL FOR THE TEAM.
```

---

MENTION THIS IS THE PROOF OF CONCEPT SHOWING COMMUNICATIONS ONLY 

## TIER 2 — THE FLEET (Demo Mode — No Docker Required)

### Step 1 — Navigate to Fleet Directory
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2"
```

---

### Step 2 — Run Fleet in Demo Mode
```bash
python3 run_fleet.py --demo
```
*~2-3 minutes. General makes real Claude API calls.*
*Scout, Phantom, Breacher all run in simulated mode.*
*No Docker containers needed.*

---

### Step 3 — Show the General's AI Reasoning (Key Moment) DID NOT WORK. JUST SHOWED NOTHING. But the fleet log had allot of info when I typed the cat version of it.music_lab@Jordans-MacBook-Air generated % ls
fleet_log.json
music_lab@Jordans-MacBook-Air generated % pwd
/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2/generated
music_lab@Jordans-MacBook-Air generated % 

Fix this for me.
```bash
python3 -c "
import json
data = json.load(open('/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2/generated/fleet_log.json'))
print('=== FLEET GENERAL — LIVE AI DECISIONS ===')
print()
for i, d in enumerate(data['decisions'], 1):
    dec = d['decision']
    print(f'Decision {i}: {d[\"situation\"].upper()}')
    print(f'  Action:  {dec.get(\"decision\", \"\")[:80]}')
    print(f'  SPARTA:  {dec.get(\"sparta_mapping\", \"\")}')
    print(f'  Crew:    {dec.get(\"crew_safety_impact\", \"\").upper()}')
    print(f'  Reason:  {dec.get(\"reasoning\", \"\")[:100]}')
    agents = dec.get(\"next_actions\", [])
    if agents:
        print(f'  Tasked:  {[a[\"agent\"] for a in agents]}')
    print()
"
```
*This is the proof the AI is reasoning, not scripting.*
*Watch crew safety escalate: none → low → high → critical*

---

WHAT SHOULD I DO AT THIS STEP. GIVE ME VIDEO NOTES TO SAY.
### Step 4 — Show Active Agents the General Deployed 
```bash
python3 -c "
import json
data = json.load(open('/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2/generated/fleet_log.json'))
state = data['mission_state']
print(f'Objective: {state[\"objective\"]}')
print(f'Status:    {state[\"status\"]}')
print(f'Agents deployed: {state[\"active_agents\"]}')
print(f'SPARTA TTPs covered: {list(state[\"sparta_mappings\"].keys())}')
print(f'Findings: {len(state[\"findings\"])}')
"
```

---

### Step 5 — Run Fleet Live Against Docker Lab (Optional — if containers running)
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2"
python3 run_fleet.py
```
*Same as demo mode but Scout, Phantom, Breacher execute against real containers.*
*Requires Docker lab running from Tier 1 steps above.*

---

## TIER 3 — SOVEREIGN PHANTOM REACH POC

### Step 1 — Navigate to Sovereign Directory
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/sovereign"
```

---
NOTE I WANT TO MOVE THIS TO RUN AT THE SAME TIME AS THE TIER 2 FLEET GENERAL DEMO. 

### Step 2 — Run PHANTOM REACH in Demo Mode (No Docker)
```bash
python3 phantom_reach_poc.py --demo
```
*~5 minutes. Press Enter to advance through each phase.*
*Side-by-side display: attack reality vs Haven-1 telemetry.*

---

### Step 3 — Run PHANTOM REACH Live (Docker Required) 
```bash
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab"
docker compose up -d && sleep 8
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/sovereign"
python3 phantom_reach_poc.py
```
*Same demo but Phase 4 actually writes to the real Modbus container.*
*O2 register genuinely spoofed in space-lifesupport container.*

---

### Step 4 — Verify Sensor Spoof Worked (Live Mode Only)
```bash
curl -s http://localhost:8083/sensors/read | python3 -m json.tool
```
*Should show: reported O2 = 20.9% but physical O2 = 14.2%*
*This is the visual proof of the attack.*

---

### Step 5 — Reset Life Support to Nominal After Demo
```bash
curl -s -X POST http://localhost:8083/sensors/reset | python3 -m json.tool
```
*Always reset after live PHANTOM REACH demo.*

---

## COMPLETE VIDEO SEQUENCE — Recommended Order

```
SCENE 1   Business case          python3 demo_business.py
          No Docker. ~4 minutes.
          "The financial case for proactive security."

SCENE 2   Lab startup            docker compose up -d
          Show 6 containers coming online.
          "The Haven-1 digital twin."

SCENE 3   AEGIS live run         python3 aegis.py
          Docker required. ~6 minutes.
          "12 steps. Zero failures. 93 gaps. 8.5 seconds."

SCENE 4   SPARTA heatmap         open heatmap.html
          Browser. ~30 seconds narration.
          "Every red cell is a technique that succeeded."

SCENE 5   OPA demo               bash defensive/opa_demo.sh
          ~1 minute.
          "6 FAIL. 6 PASS. Policy auto-generated."

SCENE 6   Fleet demo             python3 run_fleet.py --demo
          No Docker. ~3 minutes.
          "The General is reasoning in real time."

SCENE 7   General decisions      python3 -c "..." (Step 3 above)
          ~1 minute.
          "Watch crew safety escalate. Not scripted."

SCENE 8   PHANTOM REACH          python3 phantom_reach_poc.py --demo
          No Docker. ~5 minutes.
          "Left: attack. Right: telemetry. Right stays nominal."

SCENE 9   Sensor proof           curl sensors/read (live mode only)
          ~30 seconds.
          "20.9% reported. 14.2% actual."

SCENE 10  SOVEREIGN vision       Voiceover only
          ~1 minute.
          "Three years. Four components. Forty people."

TOTAL RUNTIME: ~25 minutes full presentation
               ~8 minutes highlights only
```

---

## Quick Troubleshooting

```bash
# Docker not starting
open -a Docker && sleep 30

# Container not running
cd ".../aegis/lab" && docker compose down && docker compose up -d

# API key not set
export ANTHROPIC_API_KEY=your_key_here
echo $ANTHROPIC_API_KEY

# Python path error
export PYTHONPATH="/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"

# Chain.json not found
cd ".../aegis" && python3 planner/chain_builder.py

# Results.json not found (runner path issue)
cd ".../aegis/runner"
./aegis-runner "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/chain.json"

# Heatmap blank
python3 outputs/heatmap.py
open generated/heatmap.html
```

---

## Environment Variables (Should Already Be Set)

```bash
# Verify these are set before recording
echo $ANTHROPIC_API_KEY
echo $PYTHONPATH

# If not set — add to current session
export ANTHROPIC_API_KEY=your_key_here
export PYTHONPATH="/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
```
