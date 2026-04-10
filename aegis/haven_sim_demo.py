#!/usr/bin/env python3
"""
HAVEN-SIM  ·  Jordan Rodgers
Live demo — boots real Docker lab, runs real AEGIS pipeline.
Press ENTER to advance through each slide.
"""

import sys
import time
import os
import subprocess
import re
import json
import urllib.request

BASE      = os.path.dirname(os.path.abspath(__file__))
LAB       = os.path.join(BASE, "lab")
SCENARIOS = os.path.join(BASE, "scenarios")
GENERATED = os.path.join(BASE, "generated")

class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    BLUE   = "\033[38;5;27m"
    LBLUE  = "\033[38;5;39m"
    CYAN   = "\033[38;5;45m"
    WHITE  = "\033[38;5;255m"
    GREY   = "\033[38;5;244m"
    DGREY  = "\033[38;5;238m"
    GREEN  = "\033[38;5;46m"
    YELLOW = "\033[38;5;220m"
    RED    = "\033[38;5;196m"

def clear():
    os.system("clear")

def cols():
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 110

def strip_ansi(t):
    return re.sub(r'\033\[[0-9;]*m', '', t)

def hr(char="─", color=C.BLUE):
    print(f"{color}{char * cols()}{C.RESET}")

def center(text, color=C.WHITE):
    pad = max(0, (cols() - len(strip_ansi(text))) // 2)
    print(f"{' ' * pad}{color}{text}{C.RESET}")

def typewrite(text, color=C.WHITE, delay=0.014):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(C.RESET + "\n")

def bullet(sym, sc, text, tc=C.WHITE, indent=4):
    print(f"{' ' * indent}{sc}{sym}{C.RESET}  {tc}{text}{C.RESET}")

def tag(label, color=C.BLUE):
    t = f"  [ {label} ]"
    print(f"\n{color}{C.BOLD}{t}{C.RESET}")
    print(f"{color}{'─' * (len(t) + 2)}{C.RESET}")

def pause():
    print(f"\n  {C.DGREY}▸  press {C.LBLUE}ENTER{C.DGREY} to continue ...{C.RESET}")
    input("")

def stream_cmd(cmd, cwd=None, prefix="  "):
    proc = subprocess.Popen(
        cmd, shell=isinstance(cmd, str),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, cwd=cwd
    )
    for line in proc.stdout:
        line = line.rstrip()
        if not line:
            continue
        lo = line.lower()
        if any(k in lo for k in ("error", "fail", "fatal", "critical")):
            color = C.RED
        elif any(k in lo for k in ("warn", "!!!", "bypass", "vuln", "attack", "replay", "spoof")):
            color = C.YELLOW
        elif any(k in lo for k in ("success", "complete", "accept", "ready", "health", "[+")):
            color = C.GREEN
        elif any(k in lo for k in ("step", "phase", "running", "building", "chain", "gap", "debrief")):
            color = C.LBLUE
        else:
            color = C.GREY
        print(f"{prefix}{color}{line}{C.RESET}")
    proc.wait()
    return proc.returncode

def http_get(url, timeout=3):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception:
        return None

def lab_running():
    return http_get("http://localhost:8080/health") is not None

def wait_lab(timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if lab_running():
            return True
        time.sleep(2)
    return False

def slide_title():
    clear()
    print("\n" * 3)
    hr("═", C.BLUE)
    print()
    center(f"{C.BOLD}{C.BLUE}H A V E N - S I M{C.RESET}")
    center(f"{C.LBLUE}AI-Augmented Adversary Emulation for Space Infrastructure{C.RESET}")
    print()
    hr("═", C.BLUE)
    print()
    center(f"{C.WHITE}Jordan Rodgers  ·  Staff Offensive Security Engineer{C.RESET}")
    print()
    center(f"{C.GREY}jordanrodgers.dev{C.RESET}")
    center(f"{C.GREY}github.com/jolly-rodgers{C.RESET}")
    center(f"{C.GREY}linkedin.com/in/jollyrodgers{C.RESET}")
    print("\n" * 2)
    pause()

def slide_problem():
    clear()
    print()
    hr("─", C.BLUE)
    tag("THE OPPORTUNITY", C.BLUE)
    print()
    typewrite("  Commercial space is the fastest-growing critical infrastructure sector on Earth.", C.WHITE, 0.012)
    typewrite("  And it is the last major sector without a systematic red team program.", C.LBLUE, 0.012)
    print()
    typewrite("  Here is what the attack surface looks like right now:", C.GREY, 0.011)
    print()
    time.sleep(0.2)
    bullet("▸", C.BLUE, "Ground station web interfaces exposed to the internet",        C.WHITE)
    bullet("▸", C.BLUE, "CI/CD pipelines with signing keys stored in environment vars", C.WHITE)
    bullet("▸", C.BLUE, "CCSDS uplink with no replay counter enforcement",              C.WHITE)
    bullet("▸", C.BLUE, "Life support OT reachable from ground segment network",        C.WHITE)
    bullet("▸", C.BLUE, "No SPARTA-mapped adversary emulation in commercial space",     C.WHITE)
    print()
    hr("·", C.DGREY)
    print()
    typewrite("  My plan: build the red team program that closes every one of these gaps.", C.BOLD + C.LBLUE, 0.013)
    typewrite("  Systematically. Prioritized by mission impact. Starting on day one.", C.WHITE, 0.012)
    print()
    hr("─", C.BLUE)
    pause()

def slide_business_case():
    clear()
    print()
    hr("─", C.BLUE)
    tag("THE BUSINESS CASE", C.BLUE)
    print()
    typewrite("  The real question is never technical. It is financial.", C.WHITE, 0.013)
    typewrite("  What does a breach cost vs. what does prevention cost?", C.GREY, 0.012)
    print()
    print(f"  {C.RED}{C.BOLD}COST OF A BREACH  —  Worst Case Estimate{C.RESET}")
    print()
    for item, cost in [
        ("Mission loss / vehicle failure",          "$200M - $500M"),
        ("Regulatory fines (CMMC, ITAR violation)", "$10M - $50M"),
        ("Contract loss / DoD disqualification",    "$100M+"),
        ("Incident response & forensics",           "$2M - $8M"),
        ("Reputational damage / stock impact",      "Unquantifiable"),
        ("Human safety liability",                  "Unquantifiable"),
    ]:
        pad = 48 - len(item)
        print(f"  {C.GREY}  {item}{' ' * pad}{C.RED}{C.BOLD}{cost}{C.RESET}")
        time.sleep(0.07)
    print()
    print(f"  {C.GREY}{'─' * (cols() - 4)}{C.RESET}")
    print(f"  {C.RED}  {'TOTAL EXPOSURE':48}{C.BOLD}$300M - $650M+{C.RESET}")
    print()
    time.sleep(0.3)
    print(f"  {C.GREEN}{C.BOLD}COST OF PREVENTION  —  Full Program Build{C.RESET}")
    print()
    for item, cost in [
        ("Staff red team engineer (year 1)",   "$160K - $227K"),
        ("Tooling, lab infrastructure, cloud", "$40K - $80K"),
        ("Certifications & training",          "$15K - $30K"),
        ("Year 2 junior hire",                 "$120K - $160K"),
        ("Annual program run cost (mature)",   "$400K - $600K"),
    ]:
        pad = 48 - len(item)
        print(f"  {C.GREY}  {item}{' ' * pad}{C.GREEN}{C.BOLD}{cost}{C.RESET}")
        time.sleep(0.07)
    print()
    print(f"  {C.GREY}{'─' * (cols() - 4)}{C.RESET}")
    print(f"  {C.GREEN}  {'TOTAL 4-YEAR PROGRAM COST':48}{C.BOLD}~$2M - $3.5M{C.RESET}")
    print()
    time.sleep(0.3)
    hr("·", C.DGREY)
    print()
    typewrite("  ROI: Every dollar spent on prevention returns $100-$200 in avoided breach cost.", C.BOLD + C.LBLUE, 0.013)
    typewrite("  HAVEN-SIM makes that math visible on every single finding it generates.", C.WHITE, 0.012)
    print()
    hr("─", C.BLUE)
    pause()

def slide_architecture():
    clear()
    print()
    hr("─", C.BLUE)
    tag("HAVEN-SIM  ·  LIVE LAB ARCHITECTURE", C.BLUE)
    print()
    typewrite("  Two isolated Docker networks model the real ground-to-space boundary.", C.WHITE, 0.012)
    print()
    print(f"  {C.LBLUE}{C.BOLD}VAST GROUND NETWORK{C.RESET}  {C.GREY}(vast-ground-network){C.RESET}")
    bullet("▸", C.BLUE, "ground-identity   :8080  — SSO / session auth",            C.WHITE)
    bullet("▸", C.BLUE, "ground-pipeline   :8081  — CI/CD flight software signing",  C.WHITE)
    bullet("▸", C.BLUE, "ground-station    :8084  — CCSDS uplink endpoint",          C.WHITE)
    print()
    print(f"  {C.LBLUE}{C.BOLD}HAVEN-1 SPACE NETWORK{C.RESET}  {C.GREY}(haven1-space-network){C.RESET}")
    bullet("▸", C.BLUE, "space-obc         :8082  — On-Board Computer",              C.WHITE)
    bullet("▸", C.BLUE, "space-lifesupport :8083  — ECLSS / life support OT",        C.WHITE)
    bullet("▸", C.BLUE, "space-comms       :8085  — RF / optical comms relay",       C.WHITE)
    print()
    print(f"  {C.GREY}  ground-station and space-comms bridge both networks — that bridge is the pivot path{C.RESET}")
    print()
    result = subprocess.run(
        "docker ps --format '{{.Names}}  {{.Status}}' 2>/dev/null",
        shell=True, capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        print(f"  {C.GREEN}{C.BOLD}LIVE CONTAINER STATUS:{C.RESET}")
        for line in result.stdout.strip().split("\n"):
            if any(n in line for n in ["ground", "space", "haven"]):
                sc = C.GREEN if "Up" in line else C.RED
                print(f"    {sc}{line}{C.RESET}")
    else:
        print(f"  {C.YELLOW}  Lab not running yet — will boot in next slide{C.RESET}")
    print()
    hr("─", C.BLUE)
    pause()

def slide_lab_boot():
    clear()
    print()
    hr("─", C.GREEN)
    tag("LIVE: DOCKER LAB BOOT", C.GREEN)
    print()
    if lab_running():
        print(f"  {C.GREEN}[+] Lab already running — skipping rebuild{C.RESET}\n")
        result = subprocess.run(
            "docker ps --format '{{.Names}}  {{.Ports}}  {{.Status}}'",
            shell=True, capture_output=True, text=True
        )
        for line in result.stdout.strip().split("\n"):
            if any(n in line for n in ["ground", "space", "haven"]):
                print(f"  {C.GREEN}{line}{C.RESET}")
    else:
        print(f"  {C.LBLUE}$ cd lab && docker compose up --build -d{C.RESET}\n")
        ret = stream_cmd("docker compose up --build -d", cwd=LAB)
        if ret != 0:
            print(f"\n  {C.RED}[!] Docker compose failed — check Docker Desktop is running{C.RESET}")
            pause()
            return
        print(f"\n  {C.GREY}Waiting for containers to be healthy...{C.RESET}")
        sys.stdout.flush()
        if wait_lab(60):
            print(f"  {C.GREEN}[+] All containers healthy{C.RESET}")
        else:
            print(f"  {C.YELLOW}[!] Containers slow to start — continuing anyway{C.RESET}")
    print()
    print(f"  {C.LBLUE}Health checks:{C.RESET}")
    for name, url in [
        ("ground-identity",   "http://localhost:8080/health"),
        ("ground-pipeline",   "http://localhost:8081/health"),
        ("space-obc",         "http://localhost:8082/health"),
        ("space-lifesupport", "http://localhost:8083/health"),
        ("ground-station",    "http://localhost:8084/health"),
        ("space-comms",       "http://localhost:8085/health"),
    ]:
        data = http_get(url)
        if data:
            print(f"  {C.GREEN}[+]{C.RESET}  {C.WHITE}{name:24}{C.RESET}  {C.GREEN}ONLINE{C.RESET}")
        else:
            print(f"  {C.YELLOW}[!]{C.RESET}  {C.WHITE}{name:24}{C.RESET}  {C.YELLOW}NOT RESPONDING{C.RESET}")
        time.sleep(0.1)
    print()
    hr("─", C.GREEN)
    pause()

def slide_life_support_live():
    clear()
    print()
    hr("─", C.BLUE)
    tag("LIVE: LIFE SUPPORT SENSOR READ  —  space-lifesupport:8083", C.BLUE)
    print()
    typewrite("  Reading actual sensor state from the running container...", C.GREY, 0.012)
    print()
    data = http_get("http://localhost:8083/sensors/read")
    if data:
        rep   = data.get("reported", {})
        phy   = data.get("physical", {})
        spoof = data.get("spoofing_active", False)
        print(f"  {C.LBLUE}$ curl http://localhost:8083/sensors/read{C.RESET}")
        print()
        print(f"  {C.BLUE}+- HAVEN-1 LIFE SUPPORT  ·  LIVE SENSOR STATE ──────────────────+{C.RESET}")
        print(f"  {C.BLUE}|{C.RESET}                                                              {C.BLUE}|{C.RESET}")
        print(f"  {C.BLUE}|{C.RESET}  {'SENSOR':12}  {'REPORTED (ground sees)':22}  {'PHYSICAL':10}  {C.BLUE}|{C.RESET}")
        print(f"  {C.BLUE}|{C.RESET}  {'─'*12}  {'─'*22}  {'─'*10}  {C.BLUE}|{C.RESET}")
        for key, label, nominal, thresh, direction in [
            ("o2",       "O2 %",         20.9,  16.0, "below"),
            ("co2",      "CO2 %",        0.4,   1.0,  "above"),
            ("pressure", "Pressure kPa", 101.3, 96.0, "below"),
        ]:
            rk = f"{key}_percent" if key != "pressure" else "pressure_kpa"
            r_val = rep.get(rk, nominal)
            p_val = phy.get(rk, nominal)
            danger   = p_val < thresh if direction == "below" else p_val > thresh
            p_color  = C.RED if danger else C.GREEN
            r_color  = C.GREEN if abs(r_val - p_val) < 0.01 else C.YELLOW
            print(f"  {C.BLUE}|{C.RESET}  {label:12}  {r_color}{str(r_val):22}{C.RESET}  {p_color}{str(p_val):10}{C.RESET}  {C.BLUE}|{C.RESET}")
        spoof_color = C.RED if spoof else C.GREEN
        spoof_label = "ACTIVE  <--  ATTACK IN PROGRESS" if spoof else "inactive"
        print(f"  {C.BLUE}|{C.RESET}                                                              {C.BLUE}|{C.RESET}")
        print(f"  {C.BLUE}|{C.RESET}  {'Spoofing':12}  {spoof_color}{spoof_label:34}{C.RESET}  {C.BLUE}|{C.RESET}")
        print(f"  {C.BLUE}+---------------------------------------------------------------+{C.RESET}")
    else:
        print(f"  {C.YELLOW}[!] Life support container not responding — is the lab running?{C.RESET}")
    print()
    typewrite("  This is the target. Ground ops sees reported values.", C.GREY, 0.012)
    typewrite("  When spoofing is active, the crew has no alarm. Ground sees nominal.", C.RED, 0.013)
    print()
    hr("─", C.BLUE)
    pause()

def slide_aegis_run():
    clear()
    print()
    hr("─", C.BLUE)
    tag("LIVE: AEGIS PIPELINE  —  nation_state_capture", C.BLUE)
    print()
    typewrite("  Running the full AEGIS pipeline against the live lab now.", C.WHITE, 0.012)
    typewrite("  AI generates attack chain -> Go runner executes -> gap analysis -> debrief.", C.GREY, 0.011)
    print()
    print(f"  {C.LBLUE}$ python3 aegis.py --scenario scenarios/nation_state_capture.yaml{C.RESET}")
    print()
    time.sleep(0.5)
    ret = stream_cmd(
        ["python3", os.path.join(BASE, "aegis.py"),
         "--scenario", os.path.join(SCENARIOS, "nation_state_capture.yaml")],
        cwd=BASE
    )
    if ret != 0:
        print(f"\n  {C.YELLOW}[!] Pipeline exited {ret} — check ANTHROPIC_API_KEY and lab status{C.RESET}")
    print()
    hr("─", C.BLUE)
    pause()

def slide_attack_results():
    clear()
    print()
    hr("─", C.BLUE)
    tag("LIVE: ATTACK CHAIN RESULTS", C.BLUE)
    print()
    try:
        with open(os.path.join(GENERATED, "results.json")) as f:
            results = json.load(f)
        with open(os.path.join(GENERATED, "gap_report.json")) as f:
            gaps = json.load(f)
        passed = results.get("steps_passed", 0)
        failed = results.get("steps_failed", 0)
        total  = passed + failed
        print(f"  {C.LBLUE}{C.BOLD}EXECUTION SUMMARY{C.RESET}")
        print()
        print(f"  {C.GREEN}  Steps passed:    {passed} / {total}{C.RESET}")
        print(f"  {C.RED}  Steps failed:    {failed} / {total}{C.RESET}")
        print()
        steps = results.get("steps", results.get("chain", []))
        if steps:
            print(f"  {C.LBLUE}ATTACK CHAIN:{C.RESET}")
            for i, step in enumerate(steps[:12], 1):
                status = step.get("status", step.get("result", "unknown"))
                name   = step.get("name", step.get("action", step.get("technique", f"step {i}")))
                sparta = step.get("sparta_id", step.get("sparta", ""))
                ok     = status in ("pass", "success", "passed", True)
                sym    = "[+]" if ok else "[!]"
                sc     = C.GREEN if ok else C.RED
                ss     = f"  {C.GREY}{sparta}{C.RESET}" if sparta else ""
                print(f"  {sc}  {sym}{C.RESET}  {C.WHITE}{name}{C.RESET}{ss}")
                time.sleep(0.06)
        print()
        total_gaps = gaps.get("total_gaps_found", 0)
        top_cm     = gaps.get("top_countermeasure", "")
        print(f"  {C.LBLUE}GAP ANALYSIS:{C.RESET}")
        print(f"  {C.GREY}  Total gaps found:   {C.YELLOW}{total_gaps}{C.RESET}")
        if top_cm:
            print(f"  {C.GREY}  Top countermeasure: {C.GREEN}{top_cm}{C.RESET}")
        for cm in gaps.get("ranked_countermeasures", [])[:4]:
            cm_id   = cm.get("cm_id", "")
            blocked = cm.get("chains_blocked", 0)
            safety  = cm.get("max_crew_safety_weight", 0)
            print(f"  {C.GREY}    {cm_id:30} blocks {blocked} chains  crew_safety:{safety}/10{C.RESET}")
            time.sleep(0.05)
    except FileNotFoundError:
        print(f"  {C.YELLOW}[!] No results yet — run the AEGIS slide first{C.RESET}")
    except Exception as e:
        print(f"  {C.RED}[!] Could not parse results: {e}{C.RESET}")
    print()
    hr("─", C.BLUE)
    pause()

def slide_life_support_post_attack():
    clear()
    print()
    hr("─", C.RED)
    tag("LIVE: LIFE SUPPORT  —  POST ATTACK STATE", C.RED)
    print()
    typewrite("  Reading life support state after attack chain execution...", C.GREY, 0.012)
    print()
    data = http_get("http://localhost:8083/sensors/read")
    if data:
        rep   = data.get("reported", {})
        phy   = data.get("physical", {})
        spoof = data.get("spoofing_active", False)
        delta = data.get("delta", {})
        if spoof:
            print(f"  {C.RED}{C.BOLD}SPOOFING ACTIVE  —  CREW IS UNAWARE{C.RESET}")
        else:
            print(f"  {C.GREEN}Spoofing not active — sensors nominal{C.RESET}")
        print()
        for key, label, unit, nominal in [
            ("o2",       "O2",       "%",   20.9),
            ("co2",      "CO2",      "%",   0.4),
            ("pressure", "Pressure", "kPa", 101.3),
        ]:
            rk    = f"{key}_percent" if key != "pressure" else "pressure_kpa"
            r_val = rep.get(rk, nominal)
            p_val = phy.get(rk, nominal)
            d_val = delta.get(key, 0)
            pc    = C.RED if abs(d_val) > 0.01 else C.GREEN
            print(f"  {C.WHITE}{label:12}{C.RESET}  "
                  f"reported={C.LBLUE}{r_val}{unit}{C.RESET}  "
                  f"physical={pc}{p_val}{unit}{C.RESET}  "
                  f"delta={pc}{d_val:+.2f}{C.RESET}")
            time.sleep(0.1)
        print()
        alerts = http_get("http://localhost:8083/sensors/alerts")
        if alerts and alerts.get("alerts"):
            print(f"  {C.RED}{C.BOLD}ACTIVE ALERTS:{C.RESET}")
            for a in alerts["alerts"][-5:]:
                print(f"  {C.RED}  [!!!] {a.get('alert', '')}{C.RESET}")
        else:
            print(f"  {C.GREEN}  No threshold alerts{C.RESET}")
    else:
        print(f"  {C.YELLOW}[!] Life support not responding{C.RESET}")
    print()
    print(f"  {C.BLUE}+- BUSINESS IMPACT ─────────────────────────────────────────────+{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  Attack:     Sensor spoofing via OT pivot from ground segment  {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  SPARTA:     EX-0014.03 / DE-0003                              {C.BLUE}|{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Human risk: Crew hypoxia / pressure loss — loss of life       {C.BLUE}|{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Breach cost: $500M - $1B+ (liability + mission + program)     {C.BLUE}|{C.RESET}")
    print(f"  {C.GREEN}|{C.RESET}  Fix cost:   ~$5K (network segmentation + OT auth)            {C.BLUE}|{C.RESET}")
    print(f"  {C.YELLOW}|{C.RESET}  ROI of fix: 200,000x                                        {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}+---------------------------------------------------------------+{C.RESET}")
    print()
    hr("─", C.RED)
    pause()

def slide_debrief():
    clear()
    print()
    hr("─", C.BLUE)
    tag("LIVE: AI ENGAGEMENT DEBRIEF", C.BLUE)
    print()
    debrief_path = os.path.join(GENERATED, "debrief.md")
    try:
        with open(debrief_path) as f:
            content = f.read()
        lines = content.split("\n")
        print(f"  {C.LBLUE}$ cat generated/debrief.md{C.RESET}")
        print()
        for line in lines[:60]:
            if line.startswith("# "):
                print(f"  {C.BOLD}{C.BLUE}{line}{C.RESET}")
            elif line.startswith("## "):
                print(f"  {C.LBLUE}{line}{C.RESET}")
            elif line.startswith("- ") or line.startswith("* "):
                print(f"  {C.WHITE}{line}{C.RESET}")
            elif line.strip().startswith("**") and line.strip().endswith("**"):
                print(f"  {C.YELLOW}{line}{C.RESET}")
            else:
                print(f"  {C.GREY}{line}{C.RESET}")
            time.sleep(0.02)
        if len(lines) > 60:
            print(f"\n  {C.GREY}  ... ({len(lines) - 60} more lines in generated/debrief.md){C.RESET}")
    except FileNotFoundError:
        print(f"  {C.YELLOW}[!] No debrief yet — run the AEGIS slide first{C.RESET}")
    print()
    hr("─", C.BLUE)
    pause()

def slide_tier2_vision():
    clear()
    print()
    hr("─", C.BLUE)
    tag("VISION — TIER 2  ·  18-24 MONTHS", C.BLUE)
    print()
    typewrite("  With the foundation proven, two new capabilities come online.", C.WHITE, 0.012)
    print()
    print(f"  {C.LBLUE}{C.BOLD}THE ORCHESTRATION LAYER{C.RESET}")
    print(f"  {C.GREY}  The AI agent evolves from planning tool to operational command layer.{C.RESET}")
    print()
    bullet("▸", C.BLUE, "Real-time attack path reasoning during live engagements",        C.WHITE)
    bullet("▸", C.BLUE, "Autonomous SPARTA technique selection per target context",        C.WHITE)
    bullet("▸", C.BLUE, "Continuous attack surface monitoring as infrastructure scales",   C.WHITE)
    bullet("▸", C.BLUE, "Business impact score on every finding, every engagement",        C.WHITE)
    print()
    print(f"  {C.LBLUE}{C.BOLD}THE GROUND STATION PIVOT CHAIN{C.RESET}")
    print(f"  {C.GREY}  The exact attack we just ran — formalized and expanded.{C.RESET}")
    print()
    bullet("▸", C.BLUE, "Entry:  ground-identity SSO portal",                             C.WHITE)
    bullet("▸", C.BLUE, "Pivot:  ground-station bridge to haven1-space-network",          C.WHITE)
    bullet("▸", C.BLUE, "Target: space-lifesupport ECLSS OT registers",                  C.WHITE)
    bullet("▸", C.BLUE, "Effect: sensor spoof — crew unaware, ground sees nominal",       C.WHITE)
    print()
    print(f"  {C.BLUE}+- BUSINESS IMPACT  (Tier 2) ───────────────────────────────────+{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Breach exposure:   $300M - $650M+                              {C.BLUE}|{C.RESET}")
    print(f"  {C.GREEN}|{C.RESET}  Program cost:      ~$800K cumulative (years 1-2)               {C.BLUE}|{C.RESET}")
    print(f"  {C.YELLOW}|{C.RESET}  Protection ratio:  400x - 800x                                {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}+---------------------------------------------------------------+{C.RESET}")
    print()
    hr("─", C.BLUE)
    pause()

def slide_tier3_vision():
    clear()
    print()
    hr("─", C.BLUE)
    tag("VISION — TIER 3  ·  3-4 YEARS  ·  THE FRONTIER", C.BLUE)
    print()
    typewrite("  Nobody in commercial space is here. This is the competitive moat.", C.WHITE, 0.013)
    print()
    for color, title, desc in [
        (C.BLUE,  "THE BINARY SPECIALIST",
                  "Custom fuzzer targeting CCSDS protocol parsers (space-obc APID 0x18).\n"
                  "       Zero-day research in flight-control binaries. AI-proven ROP chains."),
        (C.LBLUE, "THE FLEET GENERAL",
                  "Full orchestration layer managing attack and defense agents simultaneously.\n"
                  "       SPARTA reasoning about mission impact at full program scale."),
        (C.CYAN,  "THE STEALTH ARCHITECT",
                  "Complete ground-to-station pivot. Optical link traversal.\n"
                  "       Sensor spoof active — undetected by standard telemetry monitoring."),
        (C.WHITE, "THE DEFENSIVE GUARDIAN",
                  "AI-driven EDR for station RTOS. Detects the memory corruption we found.\n"
                  "       Hot-patches the binary in orbit. No reboot required."),
    ]:
        print(f"\n  {color}{C.BOLD}{title}{C.RESET}")
        print(f"       {C.GREY}{desc}{C.RESET}")
        time.sleep(0.2)
    print()
    print(f"  {C.BLUE}+- BUSINESS IMPACT  (Tier 3) ───────────────────────────────────+{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Breach exposure:   $500M - $1B+  (hardware + mission + life)   {C.BLUE}|{C.RESET}")
    print(f"  {C.GREEN}|{C.RESET}  Program cost:      ~$2M - $3.5M cumulative (4 years)           {C.BLUE}|{C.RESET}")
    print(f"  {C.YELLOW}|{C.RESET}  Protection ratio:  300x - 500x                                {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}+---------------------------------------------------------------+{C.RESET}")
    print()
    typewrite("  The red team discovers it. The AI writes the detection.", C.LBLUE, 0.013)
    typewrite("  Engineering patches it. In orbit. Without a reboot.", C.LBLUE, 0.013)
    typewrite("  That is the closed loop.", C.BOLD + C.BLUE, 0.014)
    print()
    hr("─", C.BLUE)
    pause()

def slide_tier_comparison():
    clear()
    print()
    hr("─", C.BLUE)
    tag("TIER 2  vs  TIER 3  ·  SIDE BY SIDE", C.BLUE)
    print()
    w   = cols()
    col = (w - 6) // 2

    def row(t2, t3, t2c=C.LBLUE, t3c=C.BLUE):
        pad = col - len(strip_ansi(t2))
        print(f"  {t2c}{t2}{C.RESET}{' ' * max(0, pad)}  {C.GREY}|{C.RESET}  {t3c}{t3}{C.RESET}")

    h2 = f"{'TIER 2  ·  18-24 MONTHS':^{col}}"
    h3 = f"{'TIER 3  ·  3-4 YEARS':^{col}}"
    print(f"  {C.LBLUE}{C.BOLD}{h2}{C.RESET}  {C.GREY}|{C.RESET}  {C.BLUE}{C.BOLD}{h3}{C.RESET}")
    print(f"  {C.GREY}{'─' * col}──+──{'─' * col}{C.RESET}")
    for t2, t3 in [
        ("CAPABILITIES",                  "CAPABILITIES"),
        ("AI Orchestration Layer",         "AI Orchestration + Binary Research"),
        ("Ground station pivot chain",     "Ground pivot + RTOS EDR"),
        ("SPARTA-mapped automation",       "SPARTA + CCSDS fuzzing + ROP"),
        ("OT/IT convergence testing",      "Full hardware-in-the-loop"),
        ("Continuous monitoring",          "Closed-loop orbital auto-patching"),
        ("", ""),
        ("THREAT COVERAGE",                "THREAT COVERAGE"),
        ("Corporate IT + OT/IT",           "Corporate + OT + Protocol + HW"),
        ("Ground-to-station pivot",        "Ground-to-station + firmware"),
        ("Web + cloud + network",          "Web + cloud + network + binary + RTOS"),
        ("", ""),
        ("BUSINESS IMPACT",                "BUSINESS IMPACT"),
        ("Breach exposure: $300M-$650M+",  "Breach exposure: $500M-$1B+"),
        ("Program cost: ~$800K",           "Program cost: ~$2M-$3.5M (4yr)"),
        ("Protection ratio: 400-800x",     "Protection ratio: 300-500x"),
        ("", ""),
        ("TEAM SIZE",                      "TEAM SIZE"),
        ("1-2 engineers",                  "3-4 engineers + research function"),
    ]:
        if t2.isupper() and t2 == t3:
            print(f"  {C.GREY}{'─' * col}──+──{'─' * col}{C.RESET}")
            row(t2, t3, C.GREY, C.GREY)
            print(f"  {C.GREY}{'─' * col}──+──{'─' * col}{C.RESET}")
        elif t2 == "":
            print(f"  {' ' * col}  {C.GREY}|{C.RESET}")
        else:
            row(t2, t3)
        time.sleep(0.05)
    print()
    hr("─", C.BLUE)
    pause()

def slide_roadmap():
    clear()
    print()
    hr("─", C.BLUE)
    tag("PROGRAM ROADMAP  ·  PROJECT AEGIS", C.BLUE)
    print()
    for color, phase, items in [
        (C.GREEN,  "YEAR 1  ·  Foundation",
                   ["Red team charter, ROE, engagement models — signed off",
                    "3 internal engagements delivered in 90 days",
                    "AEGIS deployed as standard engagement tooling",
                    "AWS attack surface baseline mapped",
                    "CMMC 2.0 offensive gap assessment delivered",
                    "Business impact report on every finding from day one"]),
        (C.LBLUE,  "YEAR 2  ·  Expansion  (Tier 2)",
                   ["OT/IT convergence assessments — live against real containers",
                    "First purple team exercise",
                    "AI orchestration layer deployed operationally",
                    "Full ground-to-life-support attack chain documented"]),
        (C.BLUE,   "YEAR 3  ·  Research",
                   ["CCSDS fuzzing against space-obc APID 0x18",
                    "Hardware-in-the-loop test environment built",
                    "First CVE disclosure or conference publication",
                    "First red team hire made"]),
        (C.CYAN,   "YEAR 4  ·  Frontier  (Tier 3)",
                   ["Continuous adversary simulation platform live",
                    "AI-driven RTOS EDR deployed",
                    "Closed-loop discovery-to-orbital-patch pipeline",
                    "Program runs without me in the room"]),
    ]:
        print(f"\n  {color}{C.BOLD}{phase}{C.RESET}")
        for item in items:
            bullet("·", color, item, C.GREY)
        time.sleep(0.1)
    print()
    hr("─", C.BLUE)
    pause()

def slide_close():
    clear()
    print("\n" * 2)
    hr("═", C.BLUE)
    print()
    center(f"{C.BOLD}{C.BLUE}H A V E N - S I M{C.RESET}")
    center(f"{C.GREY}AI-Augmented Adversary Emulation for Space Infrastructure{C.RESET}")
    print()
    hr("═", C.BLUE)
    print()
    for color, line in [
        (C.WHITE,         "  Built for Vast. Scoped to your actual threat environment."),
        (C.WHITE,         "  The containers you just watched run are your attack surface."),
        (C.WHITE,         "  The life support sensor state you saw is a real vulnerability."),
        (C.WHITE,         ""),
        (C.LBLUE,         "  The repo is live. The lab runs. The charter is written."),
        (C.BOLD + C.BLUE, "  I'm ready to build this with you."),
    ]:
        typewrite(line, color, delay=0.013)
        time.sleep(0.04)
    print()
    hr("═", C.BLUE)
    print()
    center(f"{C.WHITE}Jordan Rodgers{C.RESET}")
    print()
    center(f"{C.LBLUE}jordanrodgers.dev{C.RESET}")
    center(f"{C.LBLUE}github.com/jolly-rodgers{C.RESET}")
    center(f"{C.LBLUE}linkedin.com/in/jollyrodgers{C.RESET}")
    print("\n")
    print(f"  {C.GREEN}[ END OF PRESENTATION ]{C.RESET}\n")

SLIDES = [
    slide_title,
    slide_problem,
    slide_business_case,
    slide_architecture,
    slide_lab_boot,
    slide_life_support_live,
    slide_aegis_run,
    slide_attack_results,
    slide_life_support_post_attack,
    slide_debrief,
    slide_tier2_vision,
    slide_tier3_vision,
    slide_tier_comparison,
    slide_roadmap,
    slide_close,
]

def main():
    clear()
    print(f"\n  {C.BLUE}{C.BOLD}HAVEN-SIM  ·  Jordan Rodgers{C.RESET}")
    print(f"  {C.GREY}{len(SLIDES)} slides  ·  ENTER to advance  ·  Ctrl+C to exit{C.RESET}")
    print()
    print(f"  {C.YELLOW}Prerequisites:{C.RESET}")
    print(f"  {C.GREY}  · Docker Desktop running{C.RESET}")
    print(f"  {C.GREY}  · ANTHROPIC_API_KEY exported{C.RESET}")
    print(f"  {C.GREY}  · Run from your aegis/ directory{C.RESET}")
    print()
    input(f"  {C.LBLUE}Press ENTER to begin...{C.RESET}")
    try:
        for slide in SLIDES:
            slide()
    except KeyboardInterrupt:
        clear()
        print(f"\n  {C.GREY}Demo ended.{C.RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
