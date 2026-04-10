# Security Engineering Portfolio
## Jordan Rodgers — Vast Space Staff Offensive Security Engineer

---

## The Three-Tier Vision

```
TIER 1    AEGIS         Built. Runs today.
TIER 2    THE FLEET     POC built. Runs today.
TIER 3    SOVEREIGN     Architecture designed. Multi-year build.
```

---

## Quick Reference — Demo Commands

```bash
# API key (already in ~/.zshrc — verify with:)
echo $ANTHROPIC_API_KEY

# ── TIER 1 — AEGIS ──────────────────────────────────────────

# Start Docker lab
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab"
docker compose up -d && sleep 8

# Business demo (no Docker needed)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
python3 demo_business.py

# Live full pipeline
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
python3 aegis.py

# Skip runner (use existing results)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
python3 aegis.py --skip-runner

# OPA/Conftest policy gate demo
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
bash defensive/opa_demo.sh

# Open heatmap
open "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/heatmap.html"

# ── TIER 2 — THE FLEET ──────────────────────────────────────

# Demo mode (no Docker)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2"
python3 run_fleet.py --demo

# Live mode (Docker required)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2"
python3 run_fleet.py

# Show General's AI decisions
cat "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2/generated/fleet_log.json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for i, d in enumerate(data['decisions'], 1):
    dec = d['decision']
    print(f'Decision {i}: {d[\"situation\"]}')
    print(f'  Action:  {dec.get(\"decision\", \"\")}')
    print(f'  SPARTA:  {dec.get(\"sparta_mapping\", \"\")}')
    print(f'  Crew:    {dec.get(\"crew_safety_impact\", \"\")}')
    print()
"

# ── TIER 3 — SOVEREIGN POC ──────────────────────────────────

# PHANTOM REACH demo (no Docker)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/sovereign"
python3 phantom_reach_poc.py --demo

# PHANTOM REACH live (Docker required)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/sovereign"
python3 phantom_reach_poc.py

# ── DOCKER MANAGEMENT ───────────────────────────────────────

# Reset lab to clean state (run before any live demo)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab"
docker compose down && docker compose up -d && sleep 8

# Check lab status
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab"
docker compose ps
```

---

## Recommended 5-Minute Demo Sequence

```
0:00  Business demo
      python3 demo_business.py
      "The financial case for proactive security"

1:30  Reset lab + run AEGIS
      docker compose down && docker compose up -d && sleep 8
      python3 aegis.py
      "12 steps. Zero failures. 93 gaps. 8.5 seconds."

2:30  Open heatmap
      "Every red cell is a technique that succeeded.
       Scroll down for specific remediation code."

3:00  OPA demo
      bash defensive/opa_demo.sh
      "6 FAIL on compromised. 6 PASS on patched."

3:30  Fleet demo
      python3 run_fleet.py --demo
      "This is what year one looks like.
       The General is reasoning about Haven-1
       in real time using Claude API."

4:30  Show General decisions
      "Watch crew safety impact escalate.
       This reasoning was not scripted."

5:00  SOVEREIGN vision
      "Three years. Four components.
       Forty people living safely in space."
```

---

## Directory Structure

```
VAST Space/
├── aegis/                    Tier 1 — AEGIS
│   ├── aegis.py              Main entrypoint
│   ├── demo_business.py      Business case demo
│   ├── lab/                  Docker containers
│   ├── runner/               Go execution engine
│   ├── analysis/             Gap analyzer
│   ├── outputs/              Heatmap + debrief
│   ├── defensive/            OPA/Conftest demo
│   └── generated/            Results + reports
│
├── thevision-tier2/          Tier 2 — The Fleet
│   ├── run_fleet.py          Fleet runner
│   └── fleet/                Agent implementations
│       ├── general.py        Fleet General (AI)
│       ├── scout.py          Passive recon
│       ├── phantom.py        Credential theft
│       └── breacher.py       Exploitation
│
└── sovereign/                Tier 3 — SOVEREIGN
    ├── phantom_reach_poc.py  Stealth pivot demo
    └── docs/                 Architecture documents
```
