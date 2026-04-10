#!/bin/bash
# ============================================================
# AEGIS + THE FLEET — Demo Launch Commands
# Copy paste any block directly into terminal
# ============================================================


# ============================================================
# SETUP — Run once at start of presentation
# ============================================================

# Start Docker Desktop (wait 30 seconds after running)
open -a Docker

# Set API key


# Set Python path for Tier 1
export PYTHONPATH="/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"

# Start Haven-1 lab containers
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose up -d && sleep 8

# Verify all 6 containers are running
curl -s http://localhost:8080/health | python3 -m json.tool
curl -s http://localhost:8081/health | python3 -m json.tool
curl -s http://localhost:8082/health | python3 -m json.tool
curl -s http://localhost:8083/health | python3 -m json.tool
curl -s http://localhost:8084/health | python3 -m json.tool
curl -s http://localhost:8085/health | python3 -m json.tool


# ============================================================
# TIER 1 — AEGIS
# ============================================================

# --- Business demo (NO Docker, NO API key needed) -----------
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && python3 demo_business.py

# --- Live demo (Docker required, API key required) ----------
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && python3 aegis.py

# --- Live demo skip runner (uses existing results.json) -----
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && python3 aegis.py --skip-runner

# --- Run attack chain only ----------------------------------
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/runner" && ./aegis-runner "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/chain.json"

# --- Run gap analysis only ----------------------------------
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && python3 analysis/gap_analyzer.py "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/results.json"

# --- Open heatmap in browser --------------------------------
open "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/heatmap.html"

# --- Show AI-written debrief --------------------------------
cat "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/debrief.md"

# --- OPA/Conftest policy gate demo --------------------------
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && bash defensive/opa_demo.sh


# ============================================================
# TIER 2 — THE FLEET
# ============================================================

# --- Demo mode (NO Docker required, API key required) -------
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2" && python3 run_fleet.py --demo

# --- Live mode (Docker required, API key required) ----------
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2" && python3 run_fleet.py

# --- Show General's AI decisions from last run --------------
cat "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2/generated/fleet_log.json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('=== FLEET GENERAL — AI DECISIONS ===')
print()
for i, d in enumerate(data['decisions'], 1):
    dec = d['decision']
    print(f'Decision {i}: {d[\"situation\"]}')
    print(f'  Action:  {dec.get(\"decision\", \"\")}')
    print(f'  SPARTA:  {dec.get(\"sparta_mapping\", \"\")}')
    print(f'  Crew:    {dec.get(\"crew_safety_impact\", \"\")}')
    print(f'  Reason:  {dec.get(\"reasoning\", \"\")[:120]}')
    agents = dec.get('next_actions', [])
    if agents:
        print(f'  Tasked:  {[a[\"agent\"] for a in agents]}')
    print()
"


# ============================================================
# DOCKER — Lab management
# ============================================================

# Start lab
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose up -d

# Stop lab
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose down

# Reset lab (fresh state for demo)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose down && docker compose up -d && sleep 8

# Check lab status
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose ps

# View live logs from all containers
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose logs -f

# View logs from specific container
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose logs -f space-obc


# ============================================================
# RECOMMENDED DEMO SEQUENCE — Under 5 minutes
# ============================================================

# 1. Business case first (no Docker needed)
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && python3 demo_business.py

# 2. Reset lab to clean state
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/lab" && docker compose down && docker compose up -d && sleep 8

# 3. Run full AEGIS pipeline live
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && python3 aegis.py

# 4. Open heatmap
open "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis/generated/heatmap.html"

# 5. OPA policy gate demo
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis" && bash defensive/opa_demo.sh

# 6. Tier 2 fleet demo
cd "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2" && python3 run_fleet.py --demo

# 7. Show General's reasoning
cat "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/thevision-tier2/generated/fleet_log.json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('=== FLEET GENERAL — AI DECISIONS ===')
print()
for i, d in enumerate(data['decisions'], 1):
    dec = d['decision']
    print(f'Decision {i}: {d[\"situation\"]}')
    print(f'  Action:  {dec.get(\"decision\", \"\")}')
    print(f'  SPARTA:  {dec.get(\"sparta_mapping\", \"\")}')
    print(f'  Crew:    {dec.get(\"crew_safety_impact\", \"\")}')
    print(f'  Reason:  {dec.get(\"reasoning\", \"\")[:120]}')
    print()
"
