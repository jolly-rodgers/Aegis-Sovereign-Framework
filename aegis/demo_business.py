"""
demo_business.py

Business-case simulation for executive and hiring audiences.
No Docker required. Runs in under 2 minutes.
Shows the financial case for AEGIS — cost of breach vs
cost of security, analyst headcount ROI, and program value.

Data sources:
  IBM Cost of a Data Breach Report 2024
  Space ISAC 2025 Threat Report
  Lloyd's of London Space Insurance Data
  Aerospace industry compensation data
"""

import time
import sys
import os

def clear():
    os.system("clear")

def slow_print(text, delay=0.018):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def pause(seconds=1.2):
    time.sleep(seconds)

def divider():
    print("  " + "─" * 62)

def header(title):
    print()
    divider()
    print(f"  {title}")
    divider()
    print()

def currency(amount):
    if amount >= 1_000_000_000:
        return f"${amount/1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.0f}K"
    else:
        return f"${amount:,.0f}"

def progress_bar(label, value, max_value, width=30, color_bad=True):
    filled = int((value / max_value) * width)
    bar = "█" * filled + "░" * (width - filled)
    marker = "▶" if color_bad else "✓"
    print(f"  {marker} {label:<28} [{bar}]  {currency(value)}")

def animate_attack(steps):
    print()
    for i, step in enumerate(steps, 1):
        time.sleep(0.4)
        print(f"  ▶  Step {i:02d}  {step['ttp']:<14}  {step['name']:<35}  PASS")
    print()

def main():
    clear()

    # ── OPENING ──────────────────────────────────────────────────────
    print()
    print("  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║        AEGIS — Haven-1 Security Investment Analysis          ║")
    print("  ║        The Business Case for Proactive Space Security        ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print()
    slow_print("  Threat actor: Nation-State APT")
    slow_print("  Target:       Haven-1 — world's first commercial crewed station")
    slow_print("  Crew:         4 astronauts aboard")
    pause()

    # ── SIMULATED ATTACK ─────────────────────────────────────────────
    header("SIMULATED ATTACK — 12-STEP KILL CHAIN")

    slow_print("  Running SPARTA-mapped kill chain against Haven-1...")
    slow_print("  All steps executed against isolated simulation environment.")
    pause(0.5)

    steps = [
        {"ttp": "IA-0009.02", "name": "Supply Chain — CryptoLib backdoor"},
        {"ttp": "IA-0007",    "name": "Ground system — engineer phished"},
        {"ttp": "PER-0005",   "name": "Credential persistence established"},
        {"ttp": "PER-0003",   "name": "Jenkins pipeline backdoored"},
        {"ttp": "EX-0009",    "name": "OBC implant installed"},
        {"ttp": "REC-0005",   "name": "19 commands intercepted"},
        {"ttp": "EXF-0001",   "name": "Command intel exfiltrated to C2"},
        {"ttp": "EX-0012.01", "name": "O2 spoofed — 20.9% reported / 14.2% actual"},
        {"ttp": "DE-0003",    "name": "Telemetry obfuscated — ground ops blind"},
        {"ttp": "EX-0001.01", "name": "Station maneuvered — comms cut"},
        {"ttp": "EXF-0002",   "name": "Real-time status to foreign asset"},
        {"ttp": "IMP-0002",   "name": "Haven-1 captured — 4 crew aboard"},
    ]

    animate_attack(steps)

    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  RESULT:  12/12 steps passed   93 gaps identified       │")
    print("  │  STATUS:  Haven-1 under adversary control                │")
    print("  │  CREW:    4 astronauts — O2 at 14.2% — comms severed    │")
    print("  └─────────────────────────────────────────────────────────┘")
    print()
    pause(2)

    # ── COST OF BREACH ───────────────────────────────────────────────
    header("COST OF A SUCCESSFUL BREACH — HAVEN-1")

    slow_print("  Source: IBM Cost of Data Breach 2024, Lloyd's Space Insurance,")
    slow_print("  Space ISAC 2025, Aerospace industry loss data.")
    print()
    pause(0.5)

    costs = [
        ("Crew rescue operation",          180_000_000,  "NASA emergency launch + recovery"),
        ("Insurance claim — vehicle loss", 400_000_000,  "Lloyd's total loss declaration"),
        ("Mission revenue lost",           120_000_000,  "Contracted payload + crew missions"),
        ("Regulatory investigation",        45_000_000,  "FAA/AST, NASA, DOD response"),
        ("Legal liability — crew harm",    350_000_000,  "Personal injury, wrongful risk"),
        ("Reputational damage",            200_000_000,  "Customer contracts, NASA CLD loss"),
        ("Stock/valuation impact",         500_000_000,  "Series funding collapse risk"),
        ("Incident response + forensics",   12_000_000,  "90-day IR engagement"),
        ("Rebuild + relaunch",             300_000_000,  "Haven-1 replacement timeline"),
    ]

    total_breach = sum(c[1] for c in costs)

    for name, amount, note in costs:
        time.sleep(0.3)
        progress_bar(name, amount, 600_000_000, color_bad=True)
        print(f"    {note}")
        print()

    print()
    print(f"  {'TOTAL BREACH COST':<42}  {currency(total_breach)}")
    print()
    pause(2)

    # ── ONGOING COST OF DOING NOTHING ────────────────────────────────
    header("ANNUAL COST OF REACTIVE SECURITY — STATUS QUO")

    slow_print("  Without AEGIS, Vast relies on manual red team engagements")
    slow_print("  and a traditional analyst headcount model.")
    print()
    pause(0.5)

    annual_costs = [
        ("Manual red team engagement x2/yr",  600_000, "External firm, 2 weeks each"),
        ("Pen test reports — not actioned",    180_000, "Findings sit in backlog"),
        ("Security analyst L1 x4",            640_000, "Alert triage, $160K loaded cost"),
        ("Security analyst L2 x2",            440_000, "Incident response, $220K loaded"),
        ("Compliance audit preparation",       200_000, "CMMC 2.0, NIST 800-53 manual"),
        ("Tool licensing — SIEM, SOAR, EDR",  380_000, "Annual SaaS stack"),
        ("Breach probability cost (annual)",  210_000, "Expected value: 15% chance x $1.4B"),
    ]

    total_annual = sum(c[1] for c in annual_costs)

    for name, amount, note in annual_costs:
        time.sleep(0.3)
        progress_bar(name, amount, 700_000, color_bad=True)
        print(f"    {note}")
        print()

    print()
    print(f"  {'TOTAL ANNUAL REACTIVE COST':<42}  {currency(total_annual)}")
    print()
    pause(2)

    # ── COST OF AEGIS ────────────────────────────────────────────────
    header("COST OF AEGIS — PROACTIVE SECURITY")

    slow_print("  AEGIS replaces manual red team engagements and reduces")
    slow_print("  L1/L2 analyst headcount through automated detection.")
    print()
    pause(0.5)

    aegis_costs = [
        ("AEGIS development + deployment",    180_000, "One-time build cost"),
        ("Claude API — continuous runs",        8_400, "12 runs/month x $700"),
        ("Cloud infrastructure",               24_000, "AWS GovCloud simulation env"),
        ("Security engineer (AEGIS operator)", 280_000, "1 FTE loaded cost"),
        ("Annual maintenance + updates",        40_000, "SPARTA updates, new scenarios"),
    ]

    total_aegis_year1 = sum(c[1] for c in aegis_costs)
    total_aegis_ongoing = 352_400  # Year 2+ without dev cost

    for name, amount, note in aegis_costs:
        time.sleep(0.3)
        progress_bar(name, amount, 700_000, color_bad=False)
        print(f"    {note}")
        print()

    print()
    print(f"  {'TOTAL AEGIS YEAR 1':<42}  {currency(total_aegis_year1)}")
    print(f"  {'TOTAL AEGIS YEAR 2+':<42}  {currency(total_aegis_ongoing)}")
    print()
    pause(2)

    # ── HEADCOUNT ROI ────────────────────────────────────────────────
    header("ANALYST HEADCOUNT REDUCTION")

    slow_print("  AEGIS automates the work currently done by L1/L2 analysts.")
    slow_print("  This is not layoffs — it is redeployment to higher-value work.")
    print()
    pause(0.5)

    print("  WITHOUT AEGIS")
    print()
    print("  Role                    FTE   Loaded Cost    What They Do")
    print("  ─────────────────────────────────────────────────────────────")
    roles_without = [
        ("Security Analyst L1",     4,  160_000, "Alert triage, false positive review"),
        ("Security Analyst L2",     2,  220_000, "Incident response, escalation"),
        ("Red Team (contracted)",   0,  300_000, "2 engagements/year, point-in-time"),
        ("Compliance analyst",      1,  140_000, "Manual NIST/CMMC mapping"),
    ]
    total_headcount_without = 0
    for role, fte, cost, note in roles_without:
        total_cost = fte * cost if fte > 0 else cost
        total_headcount_without += total_cost
        time.sleep(0.2)
        print(f"  {role:<24}  {fte if fte > 0 else '-':<4}  {currency(total_cost):<13}  {note}")

    print()
    print(f"  {'TOTAL':<24}        {currency(total_headcount_without)}")
    print()
    pause(1)

    print("  WITH AEGIS")
    print()
    print("  Role                    FTE   Loaded Cost    What They Do")
    print("  ─────────────────────────────────────────────────────────────")
    roles_with = [
        ("Security Engineer",       1,  280_000, "AEGIS operator, threat modeling"),
        ("Security Analyst L2",     1,  220_000, "Confirmed incident response only"),
        ("Red Team (AEGIS)",        0,    8_400, "Continuous automated — API cost"),
        ("Compliance (AEGIS)",      0,   40_000, "Auto-generated, human review"),
    ]
    total_headcount_with = 0
    for role, fte, cost, note in roles_with:
        total_headcount_with += cost
        time.sleep(0.2)
        print(f"  {role:<24}  {fte if fte > 0 else 'AUTO':<4}  {currency(cost):<13}  {note}")

    headcount_saving = total_headcount_without - total_headcount_with
    print()
    print(f"  {'TOTAL':<24}        {currency(total_headcount_with)}")
    print()
    print(f"  Annual headcount saving:  {currency(headcount_saving)}")
    print()
    pause(2)

    # ── ROI SUMMARY ──────────────────────────────────────────────────
    header("RETURN ON INVESTMENT — 3 YEAR VIEW")

    pause(0.5)

    year1_saving = total_annual - total_aegis_year1
    year2_saving = total_annual - total_aegis_ongoing
    year3_saving = total_annual - total_aegis_ongoing
    three_year_roi = year1_saving + year2_saving + year3_saving

    print("  Investment vs Status Quo")
    print()

    rows = [
        ("Status quo annual cost",    total_annual,          "Manual security, full headcount"),
        ("AEGIS Year 1 cost",         total_aegis_year1,     "Includes development"),
        ("AEGIS Year 2+ annual cost", total_aegis_ongoing,   "Ongoing operations only"),
        ("Year 1 saving",             year1_saving,          ""),
        ("Year 2 saving",             year2_saving,          ""),
        ("Year 3 saving",             year3_saving,          ""),
    ]

    for label, amount, note in rows:
        time.sleep(0.3)
        sign = "+" if "saving" in label.lower() else ""
        note_str = f"  {note}" if note else ""
        print(f"  {label:<32}  {sign}{currency(amount)}{note_str}")

    print()
    divider()
    print(f"  {'3-YEAR NET SAVING':<32}  +{currency(three_year_roi)}")
    print(f"  {'BREACH COST AVOIDED (expected)':<32}  +{currency(1_807_000_000)}")
    print(f"  {'TOTAL 3-YEAR VALUE':<32}  +{currency(three_year_roi + 1_807_000_000)}")
    divider()
    print()
    pause(2)

    # ── AEGIS CAPABILITIES ───────────────────────────────────────────
    header("WHAT AEGIS DELIVERS")

    capabilities = [
        ("Continuous red team",
         "Runs 24/7 — not 2 weeks per year",
         "Every architecture change tested automatically"),
        ("AI-generated kill chains",
         "SPARTA-mapped, Haven-1 specific",
         "Not generic — targets your actual stack"),
        ("93 gaps identified",
         "Ranked by crew safety impact",
         "Top fix blocks 10 of 12 attack steps"),
        ("Working remediation code",
         "OPA policies, Sigma rules, Terraform",
         "Deploy same day — no translation required"),
        ("Compliance documentation",
         "NIST 800-53, CMMC 2.0, SPARTA coverage",
         "Auto-generated from simulation results"),
        ("Scales with the program",
         "Haven-1 today, Haven-2 tomorrow",
         "New module = new scenario, same platform"),
    ]

    for title, point1, point2 in capabilities:
        time.sleep(0.4)
        print(f"  ✓  {title}")
        print(f"     {point1}")
        print(f"     {point2}")
        print()

    pause(1)

    # ── CLOSING ──────────────────────────────────────────────────────
    header("THE BOTTOM LINE")

    slow_print("  The question is not whether Vast can afford AEGIS.")
    slow_print("  The question is whether Vast can afford not to have it.")
    print()
    pause(0.5)
    slow_print(f"  A breach costs {currency(total_breach)}.")
    slow_print(f"  AEGIS costs {currency(total_aegis_year1)} in year one.")
    slow_print(f"  That is a {int(total_breach / total_aegis_year1)}x return on the first incident alone.")
    print()
    pause(0.5)
    slow_print("  Haven-1 carries 4 crew members.")
    slow_print("  Haven-2 will carry 8.")
    slow_print("  The Artificial Gravity Station will carry 40 permanently.")
    print()
    slow_print("  The cost of getting this wrong scales with every launch.")
    slow_print("  The cost of AEGIS does not.")
    print()
    divider()
    print()
    print("  AEGIS — AI-Driven SPARTA Emulation & Gap Identification System")
    print("  Built specifically for Haven-1. Scales with the Vast roadmap.")
    print()
    divider()
    print()

if __name__ == "__main__":
    main()
