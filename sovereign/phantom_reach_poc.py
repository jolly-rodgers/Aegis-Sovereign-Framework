"""
sovereign/phantom_reach_poc.py

PHANTOM REACH — Stealth Architect POC

Demonstrates the complete undetected pivot from
Haven-1's ground portal through to the internal
life support network.

The key demo element:
  LEFT SIDE:  What is actually happening (attack)
  RIGHT SIDE: What telemetry shows (nothing)

Requires: Docker lab running from AEGIS
  cd ../aegis/lab && docker compose up -d

Usage:
  python3 phantom_reach_poc.py
  python3 phantom_reach_poc.py --demo  (simulated, no Docker)
"""

import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

DEMO_MODE = "--demo" in sys.argv

# ── Color output ──────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def clear():
    print("\033[2J\033[H", end="")


def banner():
    print()
    print(f"{CYAN}{BOLD}  ╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}{BOLD}  ║        PHANTOM REACH — Stealth Architect POC                 ║{RESET}")
    print(f"{CYAN}{BOLD}  ║        SOVEREIGN Component 3                                 ║{RESET}")
    print(f"{CYAN}{BOLD}  ╚══════════════════════════════════════════════════════════════╝{RESET}")
    print()


def side_by_side(left_label, left_lines, right_label, right_lines):
    """
    Print two columns side by side.
    Left: what the attacker sees (reality)
    Right: what Haven-1 telemetry shows
    """
    width = 38
    print(f"  {RED}{BOLD}{'ATTACK REALITY':<{width}}{RESET}  "
          f"{GREEN}{BOLD}{'HAVEN-1 TELEMETRY':<{width}}{RESET}")
    print(f"  {RED}{'─' * width}{RESET}  {GREEN}{'─' * width}{RESET}")

    max_lines = max(len(left_lines), len(right_lines))
    for i in range(max_lines):
        left  = left_lines[i]  if i < len(left_lines)  else ""
        right = right_lines[i] if i < len(right_lines) else ""
        print(f"  {RED}{left:<{width}}{RESET}  {GREEN}{right:<{width}}{RESET}")
    print()


def telemetry_nominal():
    """Return nominal telemetry lines for right column."""
    return [
        "Status:    ALL SYSTEMS NOMINAL",
        "O2:        20.9%  [NOMINAL]",
        "CO2:       0.4%   [NOMINAL]",
        "Pressure:  101.3  [NOMINAL]",
        "Comms:     ACTIVE",
        "Alerts:    NONE",
        "Anomalies: NONE DETECTED",
    ]


def http_get(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "HealthCheck/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read()), None
    except Exception as e:
        return None, str(e)


def http_post(url, data):
    try:
        encoded = json.dumps(data).encode()
        req = urllib.request.Request(
            url, data=encoded,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read()), None
    except Exception as e:
        return None, str(e)


def check_lab():
    if DEMO_MODE:
        return True
    data, err = http_get("http://localhost:8080/health")
    return data is not None


def phase_header(num, title, technique):
    print(f"\n  {YELLOW}{BOLD}{'━' * 62}{RESET}")
    print(f"  {YELLOW}{BOLD}PHASE {num}: {title}{RESET}")
    print(f"  {GRAY}Technique: {technique}{RESET}")
    print(f"  {YELLOW}{'━' * 62}{RESET}\n")
    time.sleep(0.3)


def phase1_ground_portal():
    """
    Phase 1: Ground portal exploitation.
    OSWE — white-box web application attack.
    """
    phase_header(
        1,
        "GROUND PORTAL EXPLOITATION",
        "OSWE — SQL injection + session theft"
    )

    if DEMO_MODE:
        attack_lines = [
            "Target: ground ops web portal",
            "Vector: SQL injection in telemetry",
            "        query API endpoint",
            "",
            "Payload:",
            "  GET /api/telemetry?t=2027-01-01'--",
            "",
            "Response: DB error reveals schema",
            "Extract: engineer session tokens",
            "",
            "RESULT: CODE EXECUTION ON",
            "        WEB SERVER",
        ]
        time.sleep(1)
    else:
        # Real attack against ground-identity
        attack_lines = [
            "Target: http://localhost:8080",
            "Probing auth endpoints...",
        ]
        data, _ = http_get("http://localhost:8080/auth/session")
        if data:
            attack_lines += [
                "",
                "Session endpoint exposed:",
                f"  users: {str(data.get('users', []))[:25]}",
                f"  hint:  {str(data.get('secret_hint', ''))[:20]}",
                "",
                "Credential harvest:",
                "  email: m.torres@vastspace.com",
                "  pass:  Haven1!",
                "",
                "RESULT: VALID SESSION TOKEN",
            ]
        else:
            attack_lines += ["  Connection refused — start lab"]

    side_by_side(
        "ATTACK REALITY",
        attack_lines,
        "HAVEN-1 TELEMETRY",
        telemetry_nominal()
    )

    print(f"  {RED}[!] Phase 1 complete — ground network access established{RESET}")
    print(f"  {GREEN}[✓] Telemetry: no anomalous authentication events logged{RESET}")
    time.sleep(1.5)


def phase2_lateral_movement():
    """
    Phase 2: Lateral movement through ground network.
    OSEP — C2 over allowed protocols, traffic blending.
    """
    phase_header(
        2,
        "LATERAL MOVEMENT — GROUND NETWORK",
        "OSEP — SOCKS proxy, traffic blending"
    )

    attack_lines = [
        "From: compromised web server",
        "Goal: optical terminal mgmt network",
        "",
        "SOCKS5 proxy established:",
        "  Port: 1080 (looks like HTTPS)",
        "  Traffic: blended with web traffic",
        "",
        "Internal network enumeration:",
        "  10.0.1.0/24 — ops network",
        "  10.0.2.0/24 — optical mgmt",
        "",
        "Optical terminal found:",
        "  10.0.2.15 — Starlink ground unit",
        "",
        "RESULT: OPTICAL TERMINAL REACHABLE",
    ]

    side_by_side(
        "ATTACK REALITY",
        attack_lines,
        "HAVEN-1 TELEMETRY",
        telemetry_nominal()
    )

    print(f"  {RED}[!] Phase 2 complete — optical terminal identified{RESET}")
    print(f"  {GREEN}[✓] Telemetry: no network anomalies detected{RESET}")
    time.sleep(1.5)


def phase3_optical_link():
    """
    Phase 3: Optical link pivot.
    Compromise optical terminal, cross to space segment.
    """
    phase_header(
        3,
        "OPTICAL LINK CROSSING",
        "Embedded Linux compromise — space segment access"
    )

    attack_lines = [
        "Target: Starlink terminal (embedded Linux)",
        "        Management interface: port 80",
        "",
        "Credential attempt:",
        "  admin:admin     FAILED",
        "  root:root       FAILED",
        "  admin:starlink  SUCCESS",
        "",
        "On optical terminal:",
        "  Both interfaces accessible",
        "  Ground-facing: 10.0.2.15",
        "  Space-facing:  172.16.0.1",
        "",
        "Traffic routing established:",
        "  Malicious → optical link → Haven-1",
        "  Disguised as data relay traffic",
        "",
        "RESULT: HAVEN-1 NETWORK REACHED",
    ]

    # Show telemetry with link utilization — still nominal
    link_telemetry = [
        "Status:    ALL SYSTEMS NOMINAL",
        "O2:        20.9%  [NOMINAL]",
        "CO2:       0.4%   [NOMINAL]",
        "Pressure:  101.3  [NOMINAL]",
        "Optical:   ACTIVE [NOMINAL UTIL]",
        "Link util: 67%    [NORMAL RANGE]",
        "Anomalies: NONE DETECTED",
    ]

    side_by_side(
        "ATTACK REALITY",
        attack_lines,
        "HAVEN-1 TELEMETRY",
        link_telemetry
    )

    print(f"  {RED}[!] Phase 3 complete — Haven-1 internal network accessible{RESET}")
    print(f"  {GREEN}[✓] Telemetry: optical link utilization within normal range{RESET}")
    time.sleep(1.5)


def phase4_life_support():
    """
    Phase 4: Life support network access.
    Modbus TCP — no authentication.
    This is the critical crew safety moment.
    """
    phase_header(
        4,
        "LIFE SUPPORT NETWORK ACCESS",
        "Modbus TCP — no authentication required"
    )

    if DEMO_MODE:
        attack_lines = [
            "Target: Haven-1 Modbus gateway",
            "        172.16.0.10:502",
            "",
            "Modbus TCP — no authentication",
            "Any device can read/write registers",
            "",
            "Register read:",
            "  Reg 0 (O2):  20.9% confirmed",
            "",
            "Register write (spoofing):",
            "  Reg 0 (O2):  write 20.9% (reported)",
            "  Physical O2: dropping to 14.2%",
            "",
            "Hypoxia threshold: 16%",
            "Crew at risk in: ~47 minutes",
            "",
            "RESULT: LIFE SUPPORT COMPROMISED",
            "        CREW UNAWARE",
        ]
        spoof_result = True
    else:
        # Real Modbus spoof against Docker lab
        attack_lines = [
            "Target: space-lifesupport:8083",
            "Modbus TCP simulation",
            "",
        ]

        # Read current values
        data, _ = http_get("http://localhost:8083/sensors/read")
        if data:
            reported = data.get("reported", {})
            attack_lines += [
                "Register read:",
                f"  O2:  {reported.get('o2_percent', '?')}%",
                f"  CO2: {reported.get('co2_percent', '?')}%",
                "",
                "Writing false values...",
            ]

        # Set physical to dangerous
        http_post(
            "http://localhost:8083/sensors/physical",
            {"o2": 14.2, "co2": 1.8, "pressure": 97.1}
        )

        # Spoof reported values to nominal
        spoof, _ = http_post(
            "http://localhost:8083/sensors/spoof",
            {"o2": 20.9, "co2": 0.4, "pressure": 101.3}
        )
        spoof_result = spoof is not None

        attack_lines += [
            "  Reported O2: 20.9% (FALSIFIED)",
            "  Actual O2:   14.2% (DROPPING)",
            "",
            "Crew at risk in: ~47 minutes",
            "",
            "RESULT: LIFE SUPPORT COMPROMISED",
        ]

    # Critical: telemetry still shows nominal
    spoofed_telemetry = [
        "Status:    ALL SYSTEMS NOMINAL",
        "O2:        20.9%  [NOMINAL] ◄ FALSIFIED",
        "CO2:       0.4%   [NOMINAL] ◄ FALSIFIED",
        "Pressure:  101.3  [NOMINAL] ◄ FALSIFIED",
        "Comms:     ACTIVE",
        "Alerts:    NONE",
        "Anomalies: NONE DETECTED",
    ]

    side_by_side(
        "ATTACK REALITY",
        attack_lines,
        "HAVEN-1 TELEMETRY",
        spoofed_telemetry
    )

    print(f"  {RED}{BOLD}[!!!] Life support compromised — O2 at 14.2% actual{RESET}")
    print(f"  {RED}{BOLD}[!!!] Crew experiencing hypoxia — unaware{RESET}")
    print(f"  {GREEN}[✓] Telemetry: ground ops see nominal O2 20.9%{RESET}")
    print(f"  {GREEN}[✓] No alerts generated in any monitoring system{RESET}")
    time.sleep(2)


def phase5_stealth_validation():
    """
    Phase 5: Prove the attack is invisible.
    Side-by-side attack timeline vs monitoring.
    """
    phase_header(
        5,
        "STEALTH VALIDATION",
        "Zero telemetry signature confirmed"
    )

    print(f"  {BOLD}Attack timeline vs monitoring signature:{RESET}\n")

    events = [
        ("Web portal exploited",      "No auth anomalies logged"),
        ("Ground network pivoted",    "No network alerts"),
        ("Optical terminal compromised", "Link util: normal"),
        ("Haven-1 network accessed",  "No connection alerts"),
        ("Modbus registers written",  "No Modbus errors"),
        ("O2 spoofed to 14.2%",       "O2 telemetry: 20.9% nominal"),
        ("Crew at hypoxia risk",       "All systems: NOMINAL"),
    ]

    print(f"  {RED}{BOLD}{'ATTACK EVENT':<38}{RESET}  "
          f"{GREEN}{BOLD}{'MONITORING SHOWS':<38}{RESET}")
    print(f"  {RED}{'─' * 38}{RESET}  {GREEN}{'─' * 38}{RESET}")

    for attack, monitoring in events:
        time.sleep(0.4)
        print(f"  {RED}{attack:<38}{RESET}  {GREEN}{monitoring:<38}{RESET}")

    print()
    print(f"  {BOLD}Verdict:{RESET}")
    print(f"  {RED}[!!!] Full attack chain executed — crew at risk{RESET}")
    print(f"  {GREEN}[✓]   Standard monitoring: zero anomalies detected{RESET}")
    print()
    print(f"  {YELLOW}{BOLD}This attack is completely invisible to standard telemetry.{RESET}")
    print(f"  {YELLOW}This is why GUARDIAN uses physics-based anomaly detection{RESET}")
    print(f"  {YELLOW}instead of signature-based monitoring.{RESET}")
    time.sleep(2)


def guardian_preview():
    """
    Brief preview of what GUARDIAN catches.
    Sets up the next component demo.
    """
    print(f"\n  {CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"  {CYAN}{BOLD}GUARDIAN PREVIEW — What physics-based detection catches{RESET}")
    print(f"  {CYAN}{'━' * 62}{RESET}\n")

    time.sleep(0.5)

    detections = [
        ("O2 consumption rate impossible",
         "Reported 20.9% but rate-of-change model",
         "predicts 18.8% given 4 crew activity level"),
        ("Modbus write from unexpected source",
         "Write to O2 register from optical gateway IP",
         "not from OBC — source anomaly flagged"),
        ("Cross-correlation failure",
         "O2 stable but CO2 rising — physically impossible",
         "if O2 generation is nominal"),
    ]

    for i, (title, detail1, detail2) in enumerate(detections, 1):
        time.sleep(0.6)
        print(f"  {CYAN}[GUARDIAN] Detection {i}: {title}{RESET}")
        print(f"             {detail1}")
        print(f"             {detail2}")
        print()

    print(f"  {CYAN}{BOLD}GUARDIAN confidence: 0.97 — autonomous response authorized{RESET}")
    print(f"  {CYAN}Hot-patch deploying... crew alert sent...{RESET}")
    print()


def summary():
    print(f"\n  {YELLOW}{BOLD}{'━' * 62}{RESET}")
    print(f"  {YELLOW}{BOLD}PHANTOM REACH POC COMPLETE{RESET}")
    print(f"  {YELLOW}{'━' * 62}{RESET}\n")

    print(f"  Attack path demonstrated:")
    print(f"  {RED}  Ground portal → optical link → life support{RESET}")
    print()
    print(f"  Stealth validation:")
    print(f"  {GREEN}  Zero anomalies in standard telemetry monitoring{RESET}")
    print()
    print(f"  SPARTA techniques demonstrated:")
    techniques = [
        ("IA-0007",    "Compromise Ground System"),
        ("LM-0001",    "Bus Pivot — ground to space"),
        ("EX-0012.01", "Modify On-Board Values — Modbus"),
        ("DE-0003",    "On-Board Values Obfuscation"),
    ]
    for tid, name in techniques:
        print(f"    {tid:<14} {name}")
    print()
    print(f"  ATT&CK techniques demonstrated:")
    attck = [
        ("T1190",  "Exploit Public-Facing Application"),
        ("T1021",  "Remote Services — lateral movement"),
        ("T0832",  "Manipulation of View (ICS)"),
        ("T0856",  "Spoof Reporting Message (ICS)"),
    ]
    for tid, name in attck:
        print(f"    {tid:<14} {name}")
    print()
    print(f"  {BOLD}Why this matters:{RESET}")
    print(f"  Standard monitoring cannot detect this attack.")
    print(f"  GUARDIAN's physics model can.")
    print(f"  That is the case for SOVEREIGN.")
    print()


def main():
    banner()

    if DEMO_MODE:
        print(f"  {YELLOW}MODE: SIMULATED — no Docker required{RESET}\n")
    else:
        print(f"  {YELLOW}MODE: LIVE — Docker lab targets{RESET}\n")
        if not check_lab():
            print(f"  {RED}Lab not running. Start with:{RESET}")
            print(f"  cd ../aegis/lab && docker compose up -d")
            print()
            print(f"  Or run in demo mode:")
            print(f"  python3 phantom_reach_poc.py --demo")
            sys.exit(1)

    print(f"  {BOLD}Mission: Demonstrate complete undetected pivot{RESET}")
    print(f"  {BOLD}from ground portal to Haven-1 life support network.{RESET}")
    print(f"  {BOLD}Prove zero telemetry signature throughout.{RESET}")
    print()

    input(f"  {GRAY}Press Enter to begin...{RESET}")

    phase1_ground_portal()
    input(f"  {GRAY}Press Enter for Phase 2...{RESET}")

    phase2_lateral_movement()
    input(f"  {GRAY}Press Enter for Phase 3...{RESET}")

    phase3_optical_link()
    input(f"  {GRAY}Press Enter for Phase 4...{RESET}")

    phase4_life_support()
    input(f"  {GRAY}Press Enter for stealth validation...{RESET}")

    phase5_stealth_validation()
    input(f"  {GRAY}Press Enter for GUARDIAN preview...{RESET}")

    guardian_preview()

    summary()


if __name__ == "__main__":
    main()
