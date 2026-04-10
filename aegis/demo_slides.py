#!/usr/bin/env python3
"""
HAVEN-SIM  ·  Slideshow
Full program vision — Tier 1, 2, and 3.
No Docker. No live execution. Press ENTER to advance.
"""

import sys, time, os, re

class C:
    RESET  = "\033[0m";  BOLD   = "\033[1m"
    BLUE   = "\033[38;5;27m";  LBLUE  = "\033[38;5;39m"
    CYAN   = "\033[38;5;45m";  WHITE  = "\033[38;5;255m"
    GREY   = "\033[38;5;244m"; DGREY  = "\033[38;5;238m"
    GREEN  = "\033[38;5;46m";  YELLOW = "\033[38;5;220m"
    RED    = "\033[38;5;196m"

def clear(): os.system("clear")
def cols():
    try: return os.get_terminal_size().columns
    except: return 110
def strip_ansi(t): return re.sub(r'\033\[[0-9;]*m', '', t)
def hr(char="─", color=C.BLUE): print(f"{color}{char * cols()}{C.RESET}")
def center(text, color=C.WHITE):
    pad = max(0, (cols() - len(strip_ansi(text))) // 2)
    print(f"{' ' * pad}{color}{text}{C.RESET}")
def typewrite(text, color=C.WHITE, delay=0.013):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    sys.stdout.write(C.RESET + "\n")
def bullet(sym, sc, text, tc=C.WHITE, indent=4):
    print(f"{' ' * indent}{sc}{sym}{C.RESET}  {tc}{text}{C.RESET}")
def tag(label, color=C.BLUE):
    t = f"  [ {label} ]"
    print(f"\n{color}{C.BOLD}{t}{C.RESET}")
    print(f"{color}{'─' * (len(t) + 2)}{C.RESET}")
def pause():
    print(f"\n  {C.DGREY}▸  press {C.LBLUE}ENTER{C.DGREY} to continue...{C.RESET}")
    input("")

# ── SLIDES ────────────────────────────────────────────────────────────────────

def slide_title():
    clear(); print("\n" * 3)
    hr("═", C.BLUE); print()
    center(f"{C.BOLD}{C.BLUE}H A V E N - S I M{C.RESET}")
    center(f"{C.LBLUE}AI-Augmented Adversary Emulation for Space Infrastructure{C.RESET}")
    print(); hr("═", C.BLUE); print()
    center(f"{C.WHITE}Jordan Rodgers  ·  Staff Offensive Security Engineer{C.RESET}")
    print()
    center(f"{C.GREY}jordanrodgers.dev{C.RESET}")
    center(f"{C.GREY}github.com/jolly-rodgers{C.RESET}")
    center(f"{C.GREY}linkedin.com/in/jollyrodgers{C.RESET}")
    print("\n"); pause()

def slide_opportunity():
    clear(); print()
    hr("─", C.BLUE)
    tag("THE OPPORTUNITY", C.BLUE); print()
    typewrite("  Commercial space is the fastest-growing critical infrastructure sector on Earth.", C.WHITE, 0.012)
    typewrite("  And it is the last major sector without a systematic red team program.", C.LBLUE, 0.012)
    print()
    typewrite("  Here is what the current attack surface looks like:", C.GREY, 0.011)
    print(); time.sleep(0.2)
    bullet("▸", C.BLUE, "Ground station web interfaces exposed to the internet",        C.WHITE)
    bullet("▸", C.BLUE, "CI/CD pipelines with signing keys stored in environment vars", C.WHITE)
    bullet("▸", C.BLUE, "CCSDS uplink with no replay counter enforcement",              C.WHITE)
    bullet("▸", C.BLUE, "Life support OT reachable from ground segment network",        C.WHITE)
    bullet("▸", C.BLUE, "No SPARTA-mapped adversary emulation in commercial space",     C.WHITE)
    print(); hr("·", C.DGREY); print()
    typewrite("  My plan: build the red team program that closes every one of these gaps.", C.BOLD + C.LBLUE, 0.013)
    typewrite("  Systematically. Prioritized by mission impact. Starting on day one.", C.WHITE, 0.012)
    print(); hr("─", C.BLUE); pause()

def slide_business_case():
    clear(); print()
    hr("─", C.BLUE)
    tag("THE BUSINESS CASE", C.BLUE); print()
    typewrite("  The real question is never technical. It is financial.", C.WHITE, 0.013)
    typewrite("  What does a breach cost vs. what does prevention cost?", C.GREY, 0.012)
    print()
    print(f"  {C.RED}{C.BOLD}COST OF A BREACH  —  Worst Case Estimate{C.RESET}\n")
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
    print(f"  {C.RED}  {'TOTAL EXPOSURE':48}{C.BOLD}$300M - $650M+{C.RESET}\n")
    time.sleep(0.3)
    print(f"  {C.GREEN}{C.BOLD}COST OF PREVENTION  —  Full Program Build{C.RESET}\n")
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
    print(f"  {C.GREEN}  {'TOTAL 4-YEAR PROGRAM COST':48}{C.BOLD}~$2M - $3.5M{C.RESET}\n")
    time.sleep(0.3); hr("·", C.DGREY); print()
    typewrite("  ROI: Every dollar spent on prevention returns $100-$200 in avoided breach cost.", C.BOLD + C.LBLUE, 0.013)
    typewrite("  HAVEN-SIM makes that math visible on every single finding it generates.", C.WHITE, 0.012)
    print(); hr("─", C.BLUE); pause()

def slide_tier1_what():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 1  ·  WHAT I BUILT TODAY", C.BLUE); print()
    typewrite("  HAVEN-SIM  ·  AEGIS Pipeline", C.BOLD + C.LBLUE, 0.013)
    typewrite("  A modular AI-augmented adversary emulation framework", C.WHITE, 0.012)
    typewrite("  purpose-built for space infrastructure attack surfaces.", C.WHITE, 0.012)
    print()
    for color, num, title, desc in [
        (C.BLUE,  "01", "SPARTA Mapping Engine",
                  "Ingests target scope -> maps to space-specific ATT&CK techniques automatically"),
        (C.LBLUE, "02", "AWS Ground Station Attack Module",
                  "Terraform lab: S3 telemetry buckets, IAM role chains, EC2 command nodes"),
        (C.CYAN,  "03", "AI Recon & Path Planning Agent",
                  "LLM reasons over recon output -> prioritizes attack paths by mission impact"),
        (C.WHITE, "04", "Business Impact Report Generator",
                  "Every finding includes breach cost estimate + remediation ROI automatically"),
        (C.GREY,  "05", "Red Team Program Charter",
                  "Day-one founding document: ROE, engagement models, CMMC 2.0 alignment"),
    ]:
        print(f"\n  {color}{C.BOLD}[{num}]{C.RESET}  {C.WHITE}{C.BOLD}{title}{C.RESET}")
        print(f"       {C.GREY}{desc}{C.RESET}")
        time.sleep(0.12)
    print(); hr("─", C.BLUE); pause()

def slide_tier1_lab():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 1  ·  LIVE LAB ARCHITECTURE", C.BLUE); print()
    typewrite("  Two isolated Docker networks model the real ground-to-space boundary.", C.WHITE, 0.012)
    print()
    print(f"  {C.LBLUE}{C.BOLD}VAST GROUND NETWORK{C.RESET}  {C.GREY}(vast-ground-network){C.RESET}")
    bullet("▸", C.BLUE, "ground-identity   :8080  — SSO / session auth",            C.WHITE)
    bullet("▸", C.BLUE, "ground-pipeline   :8081  — CI/CD flight software signing",  C.WHITE)
    bullet("▸", C.BLUE, "ground-station    :8084  — CCSDS uplink endpoint",          C.WHITE)
    print()
    print(f"  {C.LBLUE}{C.BOLD}HAVEN-1 SPACE NETWORK{C.RESET}  {C.GREY}(haven1-space-network){C.RESET}")
    bullet("▸", C.BLUE, "space-obc         :8082  — On-Board Computer (APID 0x18)", C.WHITE)
    bullet("▸", C.BLUE, "space-lifesupport :8083  — ECLSS / life support OT",       C.WHITE)
    bullet("▸", C.BLUE, "space-comms       :8085  — RF / optical comms relay",      C.WHITE)
    print()
    print(f"  {C.GREY}  ground-station + space-comms bridge both networks{C.RESET}")
    print(f"  {C.YELLOW}  that bridge is the pivot path — the attack enters from ground and reaches space{C.RESET}")
    print()
    print(f"  {C.LBLUE}{C.BOLD}VULNERABILITIES MODELED:{C.RESET}")
    bullet("▸", C.RED, "CVE-2025-29912  CryptoLib auth bypass — CCSDS command replay",      C.WHITE)
    bullet("▸", C.RED, "Pipeline signing key exposed in CI/CD environment variable",          C.WHITE)
    bullet("▸", C.RED, "Life support OT registers writable from ground network",              C.WHITE)
    bullet("▸", C.RED, "Sensor spoof: reported values diverge from physical — crew unaware", C.WHITE)
    print(); hr("─", C.BLUE); pause()

def slide_tier1_scenario():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 1  ·  SCENARIO: nation_state_capture", C.BLUE); print()
    typewrite("  Actor:     Nation-state APT", C.WHITE, 0.011)
    typewrite("  Target:    Haven-1 ground segment, CI/CD pipeline, and flight software", C.WHITE, 0.011)
    typewrite("  Objective: Capture Haven-1 and bring it under foreign government control", C.WHITE, 0.011)
    print()
    print(f"  {C.LBLUE}{C.BOLD}ATTACK CHAIN:{C.RESET}\n")
    for step in [
        ("SPA-0001", "Initial Access",       "Phish ground ops engineer — SSO credential harvested"),
        ("SPA-0042", "Auth Abuse",           "Stolen session token used against ground-identity:8080"),
        ("SPA-0117", "Pipeline Access",      "Authenticated to ground-pipeline — signing key extracted"),
        ("IA-0009",  "Supply Chain",         "Malicious artifact signed with real key, queued for uplink"),
        ("EX-0001",  "Command Replay",       "CryptoLib auth bypassed — replayed CCSDS commands sent"),
        ("EX-0014",  "Sensor Compromise",    "Life support OT registers written — physical values altered"),
        ("DE-0003",  "Sensor Spoof",         "Reported values held at nominal — ground ops see nothing"),
        ("SPA-0298", "Mission Interruption", "Station under adversary control — crew at risk"),
    ]:
        sparta, phase, desc = step
        print(f"  {C.BLUE}  {sparta:12}{C.RESET}  {C.LBLUE}{phase:22}{C.RESET}  {C.GREY}{desc}{C.RESET}")
        time.sleep(0.1)
    print()
    print(f"  {C.BLUE}+- BUSINESS IMPACT ─────────────────────────────────────────────+{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Breach cost: $500M - $1B+  (mission + liability + program)    {C.BLUE}|{C.RESET}")
    print(f"  {C.GREEN}|{C.RESET}  Fix cost:   ~$50K  (patching all modeled vulnerabilities)    {C.BLUE}|{C.RESET}")
    print(f"  {C.YELLOW}|{C.RESET}  ROI:        10,000x - 20,000x                               {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}+---------------------------------------------------------------+{C.RESET}")
    print(); hr("─", C.BLUE); pause()

def slide_tier1_report():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 1  ·  BUSINESS IMPACT REPORT  ·  SAMPLE OUTPUT", C.BLUE); print()
    typewrite("  Every finding HAVEN-SIM generates includes this automatically:", C.GREY, 0.012)
    print()
    print(f"  {C.RED}{C.BOLD}STANDARD RED TEAM REPORT:{C.RESET}")
    print(f"  {C.DGREY}+{'─'*56}+{C.RESET}")
    print(f"  {C.DGREY}|{C.RESET}  CVE-2025-29912   CVSS: 9.8   CRITICAL               {C.DGREY}|{C.RESET}")
    print(f"  {C.DGREY}|{C.RESET}  CryptoLib heap overflow — auth bypass                {C.DGREY}|{C.RESET}")
    print(f"  {C.DGREY}|{C.RESET}  Remediation: patch CryptoLib to 1.3.4               {C.DGREY}|{C.RESET}")
    print(f"  {C.DGREY}+{'─'*56}+{C.RESET}")
    print(); time.sleep(0.4)
    print(f"  {C.GREEN}{C.BOLD}HAVEN-SIM OUTPUT:{C.RESET}")
    print(f"  {C.BLUE}+{'─'*56}+{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  FINDING:  CCSDS Command Replay via CryptoLib Bypass   {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  SPARTA:   EX-0001.01 / REC-0005                       {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}                                                        {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  MISSION IMPACT:                                       {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  Adversary can replay any previously-captured command  {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  including thruster fire and attitude control.         {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  Station maneuverable by attacker C2.                 {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}                                                        {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  BUSINESS IMPACT:                                      {C.BLUE}|{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Breach exposure:    $300M - $650M+                    {C.BLUE}|{C.RESET}")
    print(f"  {C.GREEN}|{C.RESET}  Cost to fix:        ~$2K  (CryptoLib patch + IMDSv2)  {C.BLUE}|{C.RESET}")
    print(f"  {C.YELLOW}|{C.RESET}  ROI of remediation: 150,000x                         {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}                                                        {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  ENGINEER TICKET:  Patch CryptoLib — see PR template   {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  CISO BRIEF:       See executive summary p.2           {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}+{'─'*56}+{C.RESET}")
    print()
    typewrite("  Same finding. Mission context. Financial context. Two audiences. Auto-generated.", C.LBLUE, 0.013)
    print(); hr("─", C.BLUE); pause()

def slide_tier1_roadmap():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 1  ·  YEAR 1 ROADMAP  ·  FOUNDATION", C.BLUE); print()
    typewrite("  Everything in Tier 1 is executable with current skill set. Starts day one.", C.WHITE, 0.012)
    print()
    for phase, items in [
        ("MONTH 1-2  ·  Program Foundation", [
            "Red team charter, ROE, engagement models — written and signed off",
            "AEGIS deployed as standard engagement tooling",
            "SPARTA knowledge base integrated and validated",
            "Business impact reporting live on every finding",
        ]),
        ("MONTH 3-4  ·  First Engagements", [
            "Engagement 1: corporate IT attack surface",
            "Engagement 2: AWS cloud infrastructure",
            "Engagement 3: ground station web interfaces",
            "All findings delivered with mission + business impact context",
        ]),
        ("MONTH 5-6  ·  Maturity Baseline", [
            "CMMC 2.0 offensive gap assessment delivered to leadership",
            "First purple team exercise scoped and run",
            "Red team maturity Level 2 assessment presented",
            "Year 2 expansion plan proposed with budget",
        ]),
    ]:
        print(f"\n  {C.LBLUE}{C.BOLD}{phase}{C.RESET}")
        for item in items:
            bullet("·", C.BLUE, item, C.GREY)
        time.sleep(0.1)
    print(); hr("─", C.BLUE); pause()

def slide_tier2():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 2  ·  18-24 MONTHS  ·  EXPANSION", C.BLUE); print()
    typewrite("  Tier 2 = everything in Tier 1, plus two new capabilities.", C.WHITE, 0.012)
    print()
    print(f"  {C.LBLUE}{C.BOLD}THE FLEET GENERAL  ·  Orchestration Layer{C.RESET}")
    print(f"  {C.GREY}  The AI agent evolves from planning tool to operational command layer.{C.RESET}\n")
    bullet("▸", C.BLUE, "Manages attack and defense agents simultaneously",              C.WHITE)
    bullet("▸", C.BLUE, "SPARTA Framework used to reason about mission impact of each vuln", C.WHITE)
    bullet("▸", C.BLUE, "Real-time attack path selection during live engagements",       C.WHITE)
    bullet("▸", C.BLUE, "Continuous attack surface monitoring as Vast infrastructure scales", C.WHITE)
    bullet("▸", C.BLUE, "Every output CMMC 2.0 mapped and boardroom-ready automatically", C.WHITE)
    print()
    print(f"  {C.LBLUE}{C.BOLD}THE STEALTH ARCHITECT  ·  Ground-to-Station Pivot Chain{C.RESET}")
    print(f"  {C.GREY}  The scenario nobody in commercial space has modeled yet.{C.RESET}\n")
    bullet("▸", C.BLUE, "Entry:  ground station web portal — standard web vulnerability",       C.WHITE)
    bullet("▸", C.BLUE, "Pivot:  through high-bandwidth optical link to station internal net",  C.WHITE)
    bullet("▸", C.BLUE, "Target: life support network segment",                                  C.WHITE)
    bullet("▸", C.BLUE, "Method: undetected by standard telemetry monitoring throughout",        C.WHITE)
    print()
    print(f"  {C.BLUE}+- BUSINESS IMPACT  (Tier 2) ───────────────────────────────────+{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  Risk covered:      OT/IT convergence + mission systems          {C.BLUE}|{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Breach exposure:   $300M - $650M+                              {C.BLUE}|{C.RESET}")
    print(f"  {C.GREEN}|{C.RESET}  Program cost:      ~$800K cumulative (years 1-2)               {C.BLUE}|{C.RESET}")
    print(f"  {C.YELLOW}|{C.RESET}  Protection ratio:  400x - 800x                                {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}+---------------------------------------------------------------+{C.RESET}")
    print(); hr("─", C.BLUE); pause()

def slide_tier3():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 3  ·  3-4 YEARS  ·  THE FRONTIER", C.BLUE); print()
    typewrite("  Tier 3 = everything in Tier 1 and 2, plus the frontier capabilities.", C.WHITE, 0.012)
    typewrite("  Nobody in commercial space is here. This is the competitive moat.", C.LBLUE, 0.012)
    print()
    print(f"  {C.BLUE}{C.BOLD}THE BINARY SPECIALIST  ·  Protocol-Level Research{C.RESET}")
    print(f"  {C.GREY}  Requires OSED/OSEE — builds on Tier 1 CCSDS lab work.{C.RESET}\n")
    bullet("▸", C.BLUE, "Custom fuzzer targeting CCSDS protocol parsers (space-obc APID 0x18)", C.WHITE)
    bullet("▸", C.BLUE, "Zero-day research in simulated flight-control binaries",                C.WHITE)
    bullet("▸", C.BLUE, "AI agent mathematically proves ROP chain for code execution",           C.WHITE)
    bullet("▸", C.BLUE, "CVE disclosure or DEF CON / Space ISAC publication",                   C.WHITE)
    print()
    print(f"  {C.BLUE}{C.BOLD}THE DEFENSIVE GUARDIAN  ·  Closed-Loop Orbital Security{C.RESET}")
    print(f"  {C.GREY}  Requires OSDA/OSIR — the full closed loop.{C.RESET}\n")
    bullet("▸", C.BLUE, "AI-driven EDR purpose-built for station RTOS",                          C.WHITE)
    bullet("▸", C.BLUE, "Detects the exact memory corruption the red team discovered",           C.WHITE)
    bullet("▸", C.BLUE, "Automatically hot-patches the binary in orbit",                         C.WHITE)
    bullet("▸", C.BLUE, "No reboot required — zero mission interruption",                        C.WHITE)
    print()
    print(f"  {C.BLUE}+- BUSINESS IMPACT  (Tier 3) ───────────────────────────────────+{C.RESET}")
    print(f"  {C.BLUE}|{C.RESET}  Risk covered:      Protocol + RTOS + full hardware stack        {C.BLUE}|{C.RESET}")
    print(f"  {C.RED}|{C.RESET}  Breach exposure:   $500M - $1B+                                {C.BLUE}|{C.RESET}")
    print(f"  {C.GREEN}|{C.RESET}  Program cost:      ~$2M - $3.5M cumulative (4 years)           {C.BLUE}|{C.RESET}")
    print(f"  {C.YELLOW}|{C.RESET}  Protection ratio:  300x - 500x                                {C.BLUE}|{C.RESET}")
    print(f"  {C.BLUE}+---------------------------------------------------------------+{C.RESET}")
    print()
    typewrite("  The red team discovers it. The AI writes the detection.", C.LBLUE, 0.013)
    typewrite("  Engineering patches it. In orbit. Without a reboot.", C.LBLUE, 0.013)
    typewrite("  That is the closed loop.", C.BOLD + C.BLUE, 0.014)
    print(); hr("─", C.BLUE); pause()

def slide_comparison():
    clear(); print()
    hr("─", C.BLUE)
    tag("TIER 1  vs  TIER 2  vs  TIER 3  ·  SIDE BY SIDE", C.BLUE); print()
    w   = cols()
    col = max(20, (w - 8) // 3)

    def row3(t1, t2, t3, c1=C.GREEN, c2=C.LBLUE, c3=C.BLUE):
        p1 = col - len(strip_ansi(t1))
        p2 = col - len(strip_ansi(t2))
        print(f"  {c1}{t1}{C.RESET}{' '*max(0,p1)}  {C.GREY}|{C.RESET}  "
              f"{c2}{t2}{C.RESET}{' '*max(0,p2)}  {C.GREY}|{C.RESET}  {c3}{t3}{C.RESET}")

    h1 = f"{'TIER 1  ·  NOW':^{col}}"
    h2 = f"{'TIER 2  ·  18-24 MO':^{col}}"
    h3 = f"{'TIER 3  ·  3-4 YR':^{col}}"
    print(f"  {C.GREEN}{C.BOLD}{h1}{C.RESET}  {C.GREY}|{C.RESET}  {C.LBLUE}{C.BOLD}{h2}{C.RESET}  {C.GREY}|{C.RESET}  {C.BLUE}{C.BOLD}{h3}{C.RESET}")
    print(f"  {C.GREY}{'─'*col}──+──{'─'*col}──+──{'─'*col}{C.RESET}")

    rows = [
        ("CAPABILITIES",           "CAPABILITIES",              "CAPABILITIES"),
        ("SPARTA Mapping Engine",  "+ Orchestration Layer",     "+ Binary Specialist"),
        ("AWS Attack Module",      "+ Ground-Station Pivot",    "+ CCSDS Fuzzer"),
        ("AI Recon Agent",         "+ SPARTA Mission Reasoning","+ ROP Automation"),
        ("Biz Impact Reports",     "+ Stealth Pivot Chain",     "+ Defensive Guardian"),
        ("Program Charter",        "+ Continuous Monitoring",   "+ Orbital Hot-Patching"),
        ("","",""),
        ("THREAT COVERAGE",        "THREAT COVERAGE",           "THREAT COVERAGE"),
        ("Corporate IT",           "+ OT/IT Convergence",       "+ Protocol Layer"),
        ("AWS Cloud",              "+ Ground-to-Station",       "+ Binary/RTOS"),
        ("Ground Station Web",     "+ Optical Link Pivot",      "+ Hardware-in-Loop"),
        ("","",""),
        ("BUSINESS IMPACT",        "BUSINESS IMPACT",           "BUSINESS IMPACT"),
        ("Breach: $300M-$650M+",   "Breach: $300M-$650M+",     "Breach: $500M-$1B+"),
        ("Cost: ~$400K (yr1)",     "Cost: ~$800K (yr1-2)",     "Cost: ~$2M-$3.5M (4yr)"),
        ("Ratio: 500-1000x",       "Ratio: 400-800x",           "Ratio: 300-500x"),
        ("","",""),
        ("TEAM SIZE",              "TEAM SIZE",                 "TEAM SIZE"),
        ("1 engineer",             "1-2 engineers",             "3-4 + research"),
    ]
    for t1, t2, t3 in rows:
        if t1.isupper() and t1 == t2 == t3:
            print(f"  {C.GREY}{'─'*col}──+──{'─'*col}──+──{'─'*col}{C.RESET}")
            row3(t1, t2, t3, C.GREY, C.GREY, C.GREY)
            print(f"  {C.GREY}{'─'*col}──+──{'─'*col}──+──{'─'*col}{C.RESET}")
        elif t1 == "":
            print(f"  {' '*col}  {C.GREY}|{C.RESET}  {' '*col}  {C.GREY}|{C.RESET}")
        else:
            row3(t1, t2, t3)
        time.sleep(0.05)
    print(); hr("─", C.BLUE); pause()

def slide_roadmap_full():
    clear(); print()
    hr("─", C.BLUE)
    tag("FULL PROGRAM ROADMAP  ·  PROJECT AEGIS", C.BLUE); print()
    for color, phase, items in [
        (C.GREEN,  "YEAR 1  ·  Foundation  (Tier 1)", [
            "Red team charter, ROE, engagement models — signed off",
            "3 internal engagements delivered in 90 days",
            "AEGIS + SPARTA-GPT deployed as standard tooling",
            "AWS attack surface baseline mapped",
            "CMMC 2.0 offensive gap assessment delivered",
            "Business impact report on every finding from day one",
        ]),
        (C.LBLUE,  "YEAR 2  ·  Expansion  (Tier 2)", [
            "OT/IT convergence assessments begin",
            "AI Orchestration Layer deployed operationally",
            "Ground-to-station pivot chain modeled and documented",
            "First purple team exercise with defensive team",
        ]),
        (C.BLUE,   "YEAR 3  ·  Research", [
            "CCSDS protocol fuzzing program launched",
            "Hardware-in-the-loop test environment built",
            "First CVE disclosure or conference publication",
            "First red team hire made",
        ]),
        (C.CYAN,   "YEAR 4  ·  Frontier  (Tier 3)", [
            "Continuous adversary simulation platform live",
            "AI-driven RTOS EDR deployed",
            "Closed-loop discovery-to-orbital-patch pipeline",
            "Program runs without me in the room",
        ]),
    ]:
        print(f"\n  {color}{C.BOLD}{phase}{C.RESET}")
        for item in items: bullet("·", color, item, C.GREY)
        time.sleep(0.1)
    print(); hr("─", C.BLUE); pause()

def slide_close():
    clear(); print("\n" * 2)
    hr("═", C.BLUE); print()
    center(f"{C.BOLD}{C.BLUE}H A V E N - S I M{C.RESET}")
    center(f"{C.GREY}AI-Augmented Adversary Emulation for Space Infrastructure{C.RESET}")
    print(); hr("═", C.BLUE); print()
    for color, line in [
        (C.WHITE,         "  Built for Vast. Scoped to your actual threat environment."),
        (C.WHITE,         "  Grounded in what I execute today."),
        (C.WHITE,         "  Pointed at where I take this program over four years."),
        (C.WHITE,         ""),
        (C.LBLUE,         "  The repo is live. The lab runs. The charter is written."),
        (C.BOLD + C.BLUE, "  I'm ready to build this with you."),
    ]:
        typewrite(line, color, 0.013); time.sleep(0.04)
    print(); hr("═", C.BLUE); print()
    center(f"{C.WHITE}Jordan Rodgers{C.RESET}"); print()
    center(f"{C.LBLUE}jordanrodgers.dev{C.RESET}")
    center(f"{C.LBLUE}github.com/jolly-rodgers{C.RESET}")
    center(f"{C.LBLUE}linkedin.com/in/jollyrodgers{C.RESET}")
    print(f"\n  {C.GREEN}[ END OF PRESENTATION ]{C.RESET}\n")

SLIDES = [
    slide_title,
    slide_opportunity,
    slide_business_case,
    slide_tier1_what,
    slide_tier1_lab,
    slide_tier1_scenario,
    slide_tier1_report,
    slide_tier1_roadmap,
    slide_tier2,
    slide_tier3,
    slide_comparison,
    slide_roadmap_full,
    slide_close,
]

def main():
    clear()
    print(f"\n  {C.BLUE}{C.BOLD}HAVEN-SIM  ·  SLIDESHOW{C.RESET}")
    print(f"  {C.GREY}{len(SLIDES)} slides  ·  ENTER to advance  ·  Ctrl+C to exit{C.RESET}")
    print(f"  {C.GREY}No Docker required — pure presentation mode{C.RESET}\n")
    input(f"  {C.LBLUE}Press ENTER to begin...{C.RESET}")
    try:
        for slide in SLIDES: slide()
    except KeyboardInterrupt:
        clear(); print(f"\n  {C.GREY}Demo ended.{C.RESET}\n"); sys.exit(0)

if __name__ == "__main__":
    main()
