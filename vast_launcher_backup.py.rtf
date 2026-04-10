#!/usr/bin/env python3
"""
VAST Space — Master Demo Launcher
Jordan Rodgers | Staff Offensive Security Engineer

Organized around the presentation timeline:
  PRE-SHOW  — everything to stage BEFORE you walk in the room
  LIVE DEMO — demos triggered DURING specific slides
  POST-SHOW — cleanup and follow-up tools after the interview

Run from: /Users/music_lab/Documents/Security Engineer Portfolio/VAST Space
"""

import subprocess
import sys
import os
import time
import shutil
from pathlib import Path

# ─── ANSI COLORS ──────────────────────────────────────────────────────────────
R   = "\033[0;31m"
G   = "\033[0;32m"
Y   = "\033[0;33m"
C   = "\033[0;36m"
W   = "\033[1;37m"
DIM = "\033[0;90m"
M   = "\033[0;35m"   # magenta — LIVE markers
RS  = "\033[0m"

ROOT      = Path(__file__).parent.resolve()
AEGIS_DIR = ROOT / "aegis"
FLEET_DIR = ROOT / "thevision-tier2"
SOV_DIR   = ROOT / "sovereign"

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def clear():
    os.system("clear")

def banner():
    clear()
    print(f"""
{C}╔══════════════════════════════════════════════════════════════════╗
║         VAST Space — Demo Launcher                               ║
║         Jordan Rodgers | Staff Offensive Security Engineer       ║
╚══════════════════════════════════════════════════════════════════╝{RS}""")

def section(title: str, color: str = Y):
    print(f"\n{color}{'─' * 4}  {W}{title}{RS}\n")

def step(msg: str):
    print(f"{C}  ▶  {msg}{RS}")

def ok(msg: str):
    print(f"{G}  ✓  {msg}{RS}")

def warn(msg: str):
    print(f"{Y}  ⚠  {msg}{RS}")

def err(msg: str):
    print(f"{R}  ✗  {msg}{RS}")

def note(msg: str):
    print(f"{DIM}     {msg}{RS}")

def live_tag():
    return f"{M}[ LIVE ON SLIDE ]{RS}"

def run(cmd: list, cwd: Path, label: str, stream: bool = True) -> bool:
    step(f"{' '.join(str(c) for c in cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=not stream,
            text=True,
        )
        if result.returncode == 0:
            ok(f"{label} — done")
            return True
        else:
            err(f"{label} — exited {result.returncode}")
            if not stream and result.stderr:
                print(f"{DIM}{result.stderr[:400]}{RS}")
            return False
    except FileNotFoundError as exc:
        err(f"Not found: {exc}")
        return False
    except KeyboardInterrupt:
        warn("Interrupted")
        return False

def pause(msg: str = "Press ENTER to continue..."):
    try:
        input(f"\n{DIM}  {msg}{RS}\n")
    except KeyboardInterrupt:
        print()
        sys.exit(0)

def confirm(msg: str) -> bool:
    try:
        return input(f"\n{Y}  {msg} (y/N): {RS}").strip().lower() == "y"
    except KeyboardInterrupt:
        return False


# ─── PREFLIGHT ────────────────────────────────────────────────────────────────

def check_api_key() -> bool:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        err("ANTHROPIC_API_KEY not set — run: export ANTHROPIC_API_KEY=sk-ant-...")
        return False
    ok(f"ANTHROPIC_API_KEY  ({key[:12]}...)")
    return True

def check_docker() -> bool:
    try:
        r = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if r.returncode == 0:
            ok("Docker daemon running")
            return True
    except FileNotFoundError:
        pass
    warn("Docker not running — lab containers will be skipped")
    return False

def check_tool(name: str) -> bool:
    found = shutil.which(name) is not None
    if found:
        ok(f"{name}")
    else:
        warn(f"{name} not found")
    return found

def preflight() -> dict:
    section("PREFLIGHT", C)
    env = {}
    env["api_key"]  = check_api_key()
    env["docker"]   = check_docker()
    env["conftest"] = check_tool("conftest")
    env["go"]       = check_tool("go")
    if not env["api_key"]:
        print(f"\n{R}  Cannot run AI demos without API key. Set it and re-run.{RS}\n")
        sys.exit(1)
    return env


# ─── PRE-SHOW ─────────────────────────────────────────────────────────────────

def preshow_run_nation_state(env: dict):
    section("PRE-SHOW 1/4 — AEGIS Nation-State Scenario", Y)
    note("Generates: chain.json, debrief.md, heatmap.html, haven_update_policy.rego")
    note("This is the scenario behind the kill chain on slide 11.")
    note("Runtime: ~47 seconds.")
    run(
        [sys.executable, "aegis.py", "--scenario", "scenarios/nation_state_capture.yaml"],
        cwd=AEGIS_DIR,
        label="AEGIS nation_state_capture",
    )

def preshow_verify_opa_files(env: dict):
    section("PRE-SHOW 2/4 — Verify + Stage OPA Files for Slide 13", Y)
    note("Slide 13 demo: conftest rejects compromised artifact, accepts hardened one.")

    files = {
        "Compromised artifact":       AEGIS_DIR / "generated/policies/update_artifact.json",
        "Hardened artifact":          AEGIS_DIR / "generated/policies/update_artifact_hardened.json",
        "AEGIS-generated OPA policy": AEGIS_DIR / "generated/policies/haven_update_policy.rego",
    }

    all_good = True
    for label, path in files.items():
        if path.exists():
            ok(f"{label}  →  {path.name}")
        else:
            err(f"MISSING: {label}  →  {path}")
            all_good = False

    policy_dir = AEGIS_DIR / "generated/policies/policy"
    policy_src = AEGIS_DIR / "generated/policies/haven_update_policy.rego"
    if policy_src.exists():
        policy_dir.mkdir(exist_ok=True)
        shutil.copy(policy_src, policy_dir / "haven_update_policy.rego")
        ok(f"Policy staged into policy/ for conftest")
    else:
        warn("Policy file missing — run Pre-Show 1 first")
        all_good = False

    if all_good:
        ok("All OPA files staged. Slide 13 demo is ready.")
    else:
        warn("Some files missing. Run Pre-Show 1 (AEGIS scenario) first.")

def preshow_fleet_dry_run(env: dict):
    section("PRE-SHOW 3/4 — Fleet General Dry Run for Slide 15", Y)
    note("Verifies the API key works and logs a fresh fleet_log.json.")
    note("Runtime: ~60-90 seconds. Watch for NONE → MEDIUM → HIGH → CRITICAL.")
    runner = FLEET_DIR / "run_fleet.py"
    if not runner.exists():
        warn(f"run_fleet.py not found at {runner}")
        return
    run(
        [sys.executable, str(runner), "--demo"],
        cwd=FLEET_DIR,
        label="Fleet General dry run",
    )

def preshow_docker_lab(env: dict):
    section("PRE-SHOW 4/4 — Start Haven-1 Docker Lab", Y)
    if not env.get("docker"):
        warn("Docker not available — skipping")
        return
    compose = AEGIS_DIR / "lab" / "docker-compose.yml"
    if not compose.exists():
        warn(f"docker-compose.yml not found at {compose}")
        return
    note("Starting: haven-sso, haven-cicd, haven-uplink, haven-obc, haven-lifesupport, haven-comms")
    run(
        ["docker", "compose", "-f", str(compose), "up", "-d"],
        cwd=AEGIS_DIR / "lab",
        label="Haven-1 lab",
    )
    ok("Lab running. All 6 containers up.")

def run_all_preshow(env: dict):
    section("RUNNING FULL PRE-SHOW SEQUENCE", C)
    note("Runs all 4 steps in order. Takes ~3 minutes total.")
    note("Run this ~15 minutes before you walk in the room.\n")
    pause("Press ENTER to begin...")

    preshow_run_nation_state(env)
    pause("Step 1 complete — press ENTER for step 2...")

    preshow_verify_opa_files(env)
    pause("Step 2 complete — press ENTER for step 3...")

    preshow_fleet_dry_run(env)
    pause("Step 3 complete — press ENTER for step 4...")

    preshow_docker_lab(env)

    print(f"""
{G}
  ╔══════════════════════════════════════════════════════╗
  ║   PRE-SHOW COMPLETE. You are ready.                  ║
  ║                                                      ║
  ║   ✓  AEGIS output files generated                   ║
  ║   ✓  OPA policy files staged for conftest           ║
  ║   ✓  Fleet General verified via dry run             ║
  ║   ✓  Haven-1 Docker lab running                     ║
  ║                                                      ║
  ║   Terminal windows to have open:                     ║
  ║     1. This launcher  (for live demos)              ║
  ║     2. aegis/generated/policies/  (conftest)        ║
  ║     3. thevision-tier2/  (show_decisions.py)        ║
  ╚══════════════════════════════════════════════════════╝
{RS}""")


# ─── LIVE DEMOS ───────────────────────────────────────────────────────────────

def live_slide13_opa(env: dict):
    section(f"LIVE — Slide 13: OPA Policy Gate {live_tag()}", M)
    if not env.get("conftest"):
        warn("conftest not found — install: brew install conftest")
        return

    policy_dir = AEGIS_DIR / "generated/policies/policy"
    artifact   = AEGIS_DIR / "generated/policies/update_artifact.json"
    hardened   = AEGIS_DIR / "generated/policies/update_artifact_hardened.json"

    for f in [artifact, hardened, policy_dir]:
        if not Path(f).exists():
            err(f"Missing: {f}")
            warn("Run Pre-Show 2 to stage OPA files first.")
            return

    print(f"\n{W}  Step 1 — Compromised artifact, NO policy (attack succeeds){RS}")
    subprocess.run(
        ["conftest", "test", str(artifact)],
        cwd=str(AEGIS_DIR / "generated/policies"),
    )

    pause("Artifact accepted — attack path is open. Press ENTER to apply AEGIS policy...")

    print(f"\n{W}  Step 2 — Compromised artifact WITH AEGIS policy (attack blocked){RS}")
    subprocess.run(
        ["conftest", "test", str(artifact), "--policy", str(policy_dir)],
        cwd=str(AEGIS_DIR / "generated/policies"),
    )

    pause("Attack blocked at the gate. Press ENTER for clean artifact test...")

    print(f"\n{W}  Step 3 — Hardened artifact WITH policy (passes clean){RS}")
    subprocess.run(
        ["conftest", "test", str(hardened), "--policy", str(policy_dir)],
        cwd=str(AEGIS_DIR / "generated/policies"),
    )
    ok("OPA demo complete — return to deck")

def live_slide15_fleet(env: dict):
    section(f"LIVE — Slide 15: Fleet General Decisions {live_tag()}", M)
    note("Shows NONE → MEDIUM → HIGH → CRITICAL escalation from fleet_log.json.")
    note("Uses the log from the pre-show dry run — no live API call needed.")

    show = FLEET_DIR / "show_decisions.py"
    log  = FLEET_DIR / "generated/fleet_log.json"

    if not show.exists():
        warn(f"show_decisions.py not found at {show}")
        return
    if not log.exists():
        warn("fleet_log.json not found — run Pre-Show 3 (Fleet dry run) first")
        return

    run([sys.executable, str(show)], cwd=FLEET_DIR, label="Fleet decisions")
    ok("Decisions shown — return to deck")

def live_slide23_ghost(env: dict):
    section(f"LIVE — Slide 23: Ghost in the Gimbal {live_tag()}", M)
    note("Three-screen AIRAG demo. Open these simultaneously:")

    screens = [
        ("Screen 1 — Offense: Binary Specialist exploit proof",
         FLEET_DIR / "generated/fleet_log.json"),
        ("Screen 2 — AIRAG audit log: VCAP anomaly → isolation → patch",
         AEGIS_DIR / "generated/debrief.md"),
        ("Screen 3 — AEGIS heatmap: RED → GREEN",
         AEGIS_DIR / "generated/heatmap.html"),
    ]

    print()
    for label, path in screens:
        if path.exists():
            ok(f"{label}")
            note(f"    {path}")
        else:
            warn(f"Missing: {label}")
            note(f"    Expected: {path}")

    heatmap = AEGIS_DIR / "generated/heatmap.html"
    if heatmap.exists() and confirm("Open heatmap.html in browser now?"):
        subprocess.run(["open", str(heatmap)])
        ok("Heatmap opened")

    print(f"""
{M}  Walk the room through three phases:{RS}

  {W}Phase 1:{RS} Compromised research payload exploits CCSDS parser
            AIRAG detects unauthorized write() to CMG memory
            Fleet General: SPARTA T1562 — kinetic exploit chain identified

  {W}Phase 2:{RS} Dark side of Earth — no ground link
            Physics sim: 15° attitude change in 4s = hull safety violation
            Circuit break: payload air-gapped from flight-control bus

  {W}Phase 3:{RS} Binary Specialist → crash dump → buffer overflow found
            Micropatch generated → Forge signs → hot-deployed to live RTOS
            90 seconds. No reboot. No ground packet. Crew never knew.

  {DIM}"We turned a potential mission-loss event into a routine
  maintenance report."{RS}
""")


# ─── POST-SHOW ────────────────────────────────────────────────────────────────

def postshow_stop_lab(env: dict):
    section("POST-SHOW — Stop Haven-1 Docker Lab", DIM)
    if not env.get("docker"):
        warn("Docker not available")
        return
    compose = AEGIS_DIR / "lab" / "docker-compose.yml"
    if not compose.exists():
        warn(f"docker-compose.yml not found at {compose}")
        return
    run(
        ["docker", "compose", "-f", str(compose), "down"],
        cwd=AEGIS_DIR / "lab",
        label="Lab shutdown",
    )

def postshow_extra_scenarios(env: dict):
    section("POST-SHOW — Additional AEGIS Scenarios", DIM)
    note("Run if the panel asked follow-up questions about supply chain or insider threat.")
    extras = [
        ("supply_chain_vendor", "Supply Chain — malicious PyPI package via vendor"),
        ("insider_ground_ops",  "Insider — ground operator with malicious intent"),
    ]
    for scenario, label in extras:
        if confirm(f"Run {label}?"):
            run(
                [sys.executable, "aegis.py", "--scenario", f"scenarios/{scenario}.yaml"],
                cwd=AEGIS_DIR,
                label=label,
            )

def postshow_phantom_reach(env: dict):
    section("POST-SHOW — PHANTOM REACH POC", DIM)
    note("SOVEREIGN demo: ground portal → optical link → life support network.")
    note("Zero telemetry. Standard monitoring shows ALL SYSTEMS NOMINAL throughout.")
    poc = SOV_DIR / "phantom_reach_poc.py"
    if not poc.exists():
        warn(f"phantom_reach_poc.py not found at {poc}")
        return
    run([sys.executable, str(poc)], cwd=SOV_DIR, label="PHANTOM REACH")


# ─── MAIN MENU ────────────────────────────────────────────────────────────────

def main():
    banner()
    env = preflight()

    while True:
        banner()
        print(f"""
{Y}  ┌─ PRE-SHOW  ──────────────────────────────────────────────────┐{RS}
{Y}  │{RS}  Run these BEFORE you walk in the room  {DIM}(~15 min before){RS}          {Y}│{RS}
{Y}  └──────────────────────────────────────────────────────────────┘{RS}

  {C}1{RS}.  {W}Run ALL pre-show steps in sequence{RS}  {DIM}← start here{RS}
  {C}2{RS}.    Pre-Show 1 — AEGIS nation-state scenario   {DIM}generates all output files{RS}
  {C}3{RS}.    Pre-Show 2 — Verify + stage OPA files      {DIM}slide 13 ready{RS}
  {C}4{RS}.    Pre-Show 3 — Fleet General dry run         {DIM}slide 15 ready, ~90 sec{RS}
  {C}5{RS}.    Pre-Show 4 — Start Haven-1 Docker lab      {DIM}6 containers up{RS}

{M}  ┌─ LIVE DEMOS  ────────────────────────────────────────────────┐{RS}
{M}  │{RS}  Trigger DURING the presentation at the named slide           {M}│{RS}
{M}  └──────────────────────────────────────────────────────────────┘{RS}

  {C}6{RS}.  {W}SLIDE 13 — OPA policy gate{RS}            {DIM}attack blocked at CI/CD gate{RS}
  {C}7{RS}.  {W}SLIDE 15 — Fleet General decisions{RS}    {DIM}NONE→MED→HIGH→CRITICAL{RS}
  {C}8{RS}.  {W}SLIDE 23 — Ghost in the Gimbal{RS}        {DIM}three-screen AIRAG demo{RS}

{DIM}  ┌─ POST-SHOW  ─────────────────────────────────────────────────┐
  │  After the interview is done                                  │
  └──────────────────────────────────────────────────────────────┘

   9.   Stop Docker lab
  10.   Supply chain + insider scenarios  (if they asked)
  11.   PHANTOM REACH POC                (if they asked about SOVEREIGN){RS}

  {C}Q{RS}.  Quit
""")

        raw = input(f"{DIM}  Select: {RS}").strip().upper()

        if raw in ("Q", "QUIT"):
            print(f"\n{G}  Good luck in there.{RS}\n")
            break

        actions = {
            "1":  run_all_preshow,
            "2":  preshow_run_nation_state,
            "3":  preshow_verify_opa_files,
            "4":  preshow_fleet_dry_run,
            "5":  preshow_docker_lab,
            "6":  live_slide13_opa,
            "7":  live_slide15_fleet,
            "8":  live_slide23_ghost,
            "9":  postshow_stop_lab,
            "10": postshow_extra_scenarios,
            "11": postshow_phantom_reach,
        }

        fn = actions.get(raw)
        if fn:
            try:
                fn(env)
            except Exception as exc:
                err(f"Error: {exc}")
            pause("Press ENTER to return to menu...")
        else:
            warn("Invalid selection")
            time.sleep(0.8)


if __name__ == "__main__":
    main()
