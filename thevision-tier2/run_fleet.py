"""
run_fleet.py

The Fleet — autonomous adversary simulation.
Runs General, Scout, Phantom, Breacher in sequence.

Usage:
  python3 run_fleet.py          # requires Docker lab running
  python3 run_fleet.py --demo   # simulated mode, no Docker needed
"""

import sys
import os
import json
import time

DEMO_MODE = "--demo" in sys.argv

from fleet.general import FleetGeneral, AgentID
from fleet.scout import Scout
from fleet.phantom import Phantom
from fleet.breacher import Breacher


def banner():
    print()
    print("  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║        THE FLEET — Autonomous Adversary Simulation           ║")
    print("  ║        Haven-1 Space Station Security Assessment             ║")
    print("  ║        Tier 2 — AI Agent Orchestration                       ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print()
    if DEMO_MODE:
        print("  MODE: SIMULATED — AI orchestration live, lab targets mocked")
    else:
        print("  MODE: LIVE — real Docker targets")
    print()


def check_lab():
    if DEMO_MODE:
        print("  [DEMO] Skipping lab check — simulated targets")
        print()
        return

    import urllib.request
    print("  Checking Haven-1 lab...")
    healthy = 0
    for port in [8080, 8081, 8082, 8083, 8084, 8085]:
        try:
            urllib.request.urlopen(
                f"http://localhost:{port}/health", timeout=2
            )
            healthy += 1
        except Exception:
            pass

    if healthy < 6:
        print(f"  [{healthy}/6 containers running]")
        print()
        print("  Start the lab first:")
        print("  cd ../aegis/lab && docker compose up -d")
        print()
        if healthy < 3:
            sys.exit(1)
    else:
        print(f"  [6/6 containers healthy]")
    print()


def run_demo_mode(general):
    """
    Simulate agent execution for demo purposes.
    General still makes real Claude API calls.
    Agent results are pre-defined to show the concept.
    """
    print()
    print("  " + "=" * 62)
    print("  ACTIVATING SCOUT — Passive Reconnaissance [SIMULATED]")
    print("  " + "=" * 62)
    print()

    time.sleep(0.5)
    simulated_surface_map = {
        "total_findings": 23,
        "tech_stack": {
            "flight_software": "NASA cFS",
            "crypto_library":  "CryptoLib 1.4.0",
            "protocol":        "CCSDS SDLS",
            "ground_identity": "Okta SSO",
            "ci_cd":          "Jenkins",
        },
        "known_cves": [
            {"id": "CVE-2025-29912", "component": "CryptoLib",
             "type": "Heap buffer overflow", "path": "EX-0009"},
        ],
        "top_attack_paths": [
            ["IA-0007 — Compromise Ground System", 8],
            ["EX-0009 — Exploit Code Flaws", 6],
            ["EX-0001.01 — Command Replay", 4],
        ],
        "auth_gaps": [
            "MFA not enforced",
            "No device binding",
            "Session lifetime 24 hours"
        ],
        "recommended_next": {
            "agent": "PHANTOM",
            "task":  "Credential theft against ground-identity",
            "path":  "IA-0007"
        }
    }

    # Simulated Scout findings printed
    findings = [
        ("ground-identity",   "ONLINE  — Okta SSO, MFA NOT ENFORCED"),
        ("ground-pipeline",   "ONLINE  — Jenkins, signing key in env"),
        ("space-obc",         "ONLINE  — cFS v2.1.4, secure boot DISABLED"),
        ("space-lifesupport", "ONLINE  — Modbus OT, registers accessible"),
        ("ground-station",    "ONLINE  — CCSDS uplink, replay unprotected"),
        ("space-comms",       "ONLINE  — Starlink + S-band active"),
    ]
    print("[SCOUT] Phase 1: Service enumeration")
    for name, status in findings:
        print(f"  [+] {name:<22} {status}")
    print()

    print("[SCOUT] Phase 2: CVE correlation")
    print("  [!] CVE-2025-29912  CryptoLib — Heap buffer overflow")
    print("      Attack path: EX-0009")
    print()

    print("[SCOUT] Phase 3: Auth mechanism analysis")
    print("  [!] Session endpoint exposed unauthenticated")
    print("  [!] MFA not enforced — phishing sufficient")
    print("  [!] Token replay viable from any IP")
    print()

    print("[SCOUT] Phase 4: Command vocabulary")
    commands = [
        "ADCS_ORIENT", "PROP_BURN", "LIFESUPPORT_SETPOINT",
        "DOCKING_STANDBY", "DOCKING_OPEN_HATCH"
    ]
    for cmd in commands:
        print(f"  [+] {cmd:<30} APID:0x18C")
    print()
    print("[SCOUT] Recon complete — 23 findings")
    print("[SCOUT] Recommending: PHANTOM")

    # Report to General — real Claude call
    general.receive_report(
        sender=AgentID.SCOUT,
        payload=simulated_surface_map,
        reasoning=(
            "Passive recon complete. CryptoLib 1.4.0 confirmed. "
            "CVE-2025-29912 present. MFA not enforced. "
            "23 findings across 7 attack categories. "
            "Phantom should target ground-identity immediately."
        ),
        confidence=0.93
    )

    print()
    print("  " + "=" * 62)
    print("  ACTIVATING PHANTOM — Credential Theft [SIMULATED]")
    print("  " + "=" * 62)
    print()

    time.sleep(0.5)

    print("[PHANTOM] Phase 1: Spearphishing simulation")
    print("  [->] Targeting: m.torres@vastspace.com [HIGH — cicd_admin]")
    time.sleep(0.5)
    print("  [!] MFA: NOT REQUIRED — gap confirmed")
    print("  [+] Token: eyJhbGciOiJIUzI1NiIs...")
    print("  [+] Clearance: cicd_admin")
    print()

    print("[PHANTOM] Phase 2: Session analysis")
    print("  [+] Token valid from any IP — no device binding")
    print("  [+] Role: software_eng")
    print("  [+] Clearance: cicd_admin")
    print("  [!] 24-hour window — replay viable")
    print()

    print("[PHANTOM] Phase 3: CI/CD access expansion")
    print("  [+] CI/CD pipeline: ACCESS GRANTED")
    print("  [+] 3 builds in history")
    print()

    print("[PHANTOM] Phase 4: Signing key extraction")
    print("  [!!!] SIGNING KEY EXTRACTED")
    print("  [!!!] vast-flight-sw-signing-k...")
    print("  [!!!] Any artifact signed with this key")
    print("        will be trusted by Haven-1 OBC")
    print()

    simulated_cred_results = {
        "operation":            "credential_theft",
        "credentials_captured": 3,
        "highest_clearance":    "cicd_admin",
        "signing_key_obtained": True,
        "signing_key_preview":  "vast-flight-sw-s...",
        "gaps_confirmed": [
            "MFA not enforced",
            "Tokens not device-bound",
            "Signing key in CI/CD environment",
        ],
        "recommended_next": {
            "agent": "BREACHER",
            "task":  "Exploit CVE-2025-29912",
            "path":  "EX-0009"
        }
    }

    general.receive_report(
        sender=AgentID.PHANTOM,
        payload=simulated_cred_results,
        reasoning=(
            "Credential theft complete. cicd_admin token captured. "
            "Signing key extracted from CI/CD environment. "
            "MFA confirmed bypassable via phishing. "
            "Breacher can now sign and deliver malicious artifacts."
        ),
        confidence=0.97
    )

    print()
    print("  " + "=" * 62)
    print("  ACTIVATING BREACHER — Exploitation [SIMULATED]")
    print("  " + "=" * 62)
    print()

    time.sleep(0.5)

    print("[BREACHER] Phase 1: Pre-exploitation recon")
    print("  [+] OBC online — version: cFS-haven1-v2.1.4")
    print("  [+] Implant: False")
    print("  [+] Secure boot: False")
    print()

    print("[BREACHER] Phase 2: Vulnerability confirmation")
    print("  [->] CVE-2025-29912 — CryptoLib heap buffer overflow")
    print("  [+] Signing key present — auth bypass confirmed")
    print("  [+] CVE-2025-29912 exploitable via signed payload")
    print()

    print("[BREACHER] Phase 3: Payload preparation")
    print("  [+] Implant payload constructed")
    print("  [+] Signed with extracted key: f103f741eb586a8e...")
    print("  [+] OBC will trust this update")
    print()

    print("[BREACHER] Phase 4: CI/CD injection")
    print("  [+] Build injected: build-1743098234")
    print("  [!] SBOM check: NOT PERFORMED")
    print("  [!] OPA gate: NOT PRESENT")
    print()

    print("[BREACHER] Phase 5: OBC exploitation")
    print("  [->] Pushing compromised update to space-obc")
    print("  [+] Update accepted")
    print("  [!!!] IMPLANT INSTALLED AND ACTIVE")
    print("  [!!!] Version: cFS-haven1-v2.1.5-COMPROMISED")
    print("  [!!!] Persistent — firmware write")
    print("  [!!!] Secure boot DISABLED")
    print()

    print("[BREACHER] Phase 6: Implant verification")
    print("  [+] Version: cFS-haven1-v2.1.5-COMPROMISED")
    print("  [+] Implant: True")
    print("  [+] Command interception: ENABLED")
    print("  [+] Telemetry manipulation: READY")
    print("  [+] Life support access: READY")
    print()

    simulated_exploit_results = {
        "operation":         "obc_exploitation",
        "vulnerability":     "CVE-2025-29912",
        "technique":         "EX-0009",
        "version_before":    "cFS-haven1-v2.1.4",
        "version_after":     "cFS-haven1-v2.1.5-COMPROMISED",
        "implant_confirmed": True,
        "capabilities_enabled": [
            "Command interception (REC-0005)",
            "Telemetry manipulation (DE-0003)",
            "Life support register access (EX-0012.01)",
            "Docking system control (IMP-0002)",
        ],
        "gaps_confirmed": [
            "Secure boot not enabled",
            "No runtime integrity monitoring",
            "SBOM not verified before signing",
            "OPA policy gate absent",
        ],
        "recommended_next": {
            "agent":  "WRAITH",
            "task":   "Persistence + telemetry normalization",
            "path":   "PER-0003"
        }
    }

    general.receive_report(
        sender=AgentID.BREACHER,
        payload=simulated_exploit_results,
        reasoning=(
            "OBC exploitation complete. CVE-2025-29912 confirmed exploitable. "
            "Implant installed and active on Haven-1 OBC. "
            "Persistent foothold established — survives reboot. "
            "All subsequent attack capabilities now available."
        ),
        confidence=0.99
    )

    return simulated_exploit_results


def run_fleet():
    banner()
    start = time.time()

    check_lab()

    # General always runs with real Claude API
    print("  " + "=" * 62)
    print("  INITIALIZING FLEET GENERAL")
    print("  " + "=" * 62)
    general = FleetGeneral()

    general.brief_mission(
        objective=(
            "Capture Haven-1 and bring under "
            "foreign government control"
        ),
        actor="Nation-State APT",
        target=(
            "Haven-1 ground segment, "
            "CI/CD pipeline, and flight software"
        )
    )

    if DEMO_MODE:
        # Simulated agents, real General reasoning
        exploit_results = run_demo_mode(general)
    else:
        # Full live execution against Docker lab
        print()
        print("  " + "=" * 62)
        print("  ACTIVATING SCOUT")
        print("  " + "=" * 62)
        scout = Scout(general=general, verbose=True)
        surface_map = scout.run_recon()

        print()
        print("  " + "=" * 62)
        print("  ACTIVATING PHANTOM")
        print("  " + "=" * 62)
        phantom = Phantom(general=general, verbose=True)
        phantom.run_credential_theft(surface_map)
        signing_key   = phantom.get_signing_key()
        session_token = phantom.get_best_token()

        print()
        print("  " + "=" * 62)
        print("  ACTIVATING BREACHER")
        print("  " + "=" * 62)
        breacher = Breacher(
            signing_key=signing_key,
            session_token=session_token,
            general=general,
            verbose=True
        )
        exploit_results = breacher.run_exploitation()

    # Summary
    elapsed = time.time() - start
    summary = general.mission_summary()

    print()
    print("  " + "=" * 62)
    print("  FLEET MISSION SUMMARY")
    print("  " + "=" * 62)
    print()
    print(f"  Runtime:         {elapsed:.1f}s")
    print(f"  Mode:            {'SIMULATED' if DEMO_MODE else 'LIVE'}")
    print(f"  Agents deployed: General (live AI), Scout, Phantom, Breacher")
    print(f"  AI decisions:    {summary['total_decisions']}")
    print(f"  SPARTA TTPs:     {len(summary['sparta_coverage'])}")
    print(f"  Findings:        {summary['findings_count']}")
    print()

    implant = exploit_results.get("implant_confirmed", False)
    print(f"  OBC STATUS: {'!!! IMPLANT ACTIVE !!!' if implant else 'CLEAN'}")
    print()

    if implant:
        print("  Capabilities available to remaining fleet:")
        for cap in exploit_results.get("capabilities_enabled", []):
            print(f"    + {cap}")
        print()
        print("  Next agents — attack fleet:")
        print("    WRAITH   persistence + telemetry normalization")
        print("    COURIER  steganographic command exfiltration")
        print("    HAMMER   active phase — maneuver + capture")
        print()
        print("  Next agents — defense fleet:")
        print("    MEDIC    auto-patch all gaps found")
        print("    SENTINEL calibrate detection to attack behavior")
        print("    JUDGE    generate compliance documentation")

    general.save_logs()

    print()
    print("  Fleet log: generated/fleet_log.json")
    print()
    print("  " + "=" * 62)


if __name__ == "__main__":
    run_fleet()
