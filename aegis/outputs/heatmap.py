import json
import os
import sys
from datetime import datetime


def load_json(path):
    with open(path) as f:
        return json.load(f)


REMEDIATION = {
    "IA-0009.02": {
        "title": "Supply Chain Compromise - Vendor",
        "how": "APT infiltrated NASA cFS CryptoLib GitHub over 18 months. Introduced CVE-2025-29912 heap buffer overflow disguised as legitimate code. Jenkins pipeline signed the artifact without content verification. No SBOM tracking detected the malicious dependency.",
        "fix": "# OPA/Conftest policy - blocks this attack\npackage haven.update_policy\n\ndeny contains msg if {\n    not input.sbom_verified\n    msg := \"REJECTED: SBOM required (CM0034) - NIST SA-12\"\n}\ndeny contains msg if {\n    input.cryptolib_version == \"1.4.0\"\n    msg := \"REJECTED: CryptoLib 1.4.0 vulnerable - CVE-2025-29912\"\n}\ndeny contains msg if {\n    not input.build_provenance\n    msg := \"REJECTED: Build provenance missing - NIST SR-4\"\n}",
        "nist": "SA-12, SA-12(1), SR-4",
        "cm": "CM0034, CM0035"
    },
    "IA-0007": {
        "title": "Compromise Ground System",
        "how": "Engineer spearphished via fake Okta SSO login. Session token captured post-MFA with no device binding or geo-check. Single compromised session gave full Jenkins CI/CD access with flight software build authority.",
        "fix": "# Okta policy\n# Require FIDO2 hardware token\n# Disable SMS/TOTP/push - phishable methods\n# Bind session to device attestation\n# Max session lifetime: 4 hours\n\n# AWS - enforce MFA on all ground ops actions\nCondition: { BoolIfExists: { aws:MultiFactorAuthPresent: false } }",
        "nist": "IA-2(1), IA-2(12), AC-17",
        "cm": "CM0001, CM0002, CM0003"
    },
    "PER-0005": {
        "title": "Credentialed Persistence",
        "how": "APT harvested Okta refresh tokens and AWS IAM keys. Tokens stored at C2. Valid until explicitly revoked. Vast did not know to revoke them. Access maintained even after engineer password reset.",
        "fix": "# Revoke ALL sessions on password change\n# Impossible travel detection in Okta\n# Maximum refresh token lifetime: 8 hours\n# Require re-auth for sensitive CI/CD operations\n# Alert on concurrent sessions from multiple geolocations",
        "nist": "IA-2, IA-5, AC-2",
        "cm": "CM0001, CM0038"
    },
    "PER-0003": {
        "title": "Ground System Presence",
        "how": "APT modified Jenkins shared library to inject persistence payload into every cFS build. Backdoored plugin survives Jenkins updates. Every new build re-implants the OBC automatically.",
        "fix": "#!/bin/bash\n# Jenkins config integrity check\nEXPECTED=$(cat .jenkins-baseline.sha256)\nACTUAL=$(sha256sum Jenkinsfile jenkins-shared-lib/* | sha256sum)\nif [ \"$EXPECTED\" != \"$ACTUAL\" ]; then\n    echo \"CRITICAL: Jenkins config tampered\"\n    exit 1\nfi",
        "nist": "CM-7, SI-3, AU-6",
        "cm": "CM0036, CM0037"
    },
    "EX-0009": {
        "title": "Exploit Code Flaws",
        "how": "Compromised cFS update exploited CryptoLib CVE-2025-29912 heap buffer overflow achieving arbitrary code execution on OBC. Implant wrote to protected firmware region surviving reboots. No secure boot or runtime integrity monitoring detected it.",
        "fix": "// cFS startup integrity check\nKNOWN_GOOD_HASHES = { crypto_app: \"a9b8c7d6...\", telemetry_app: \"f1e2d3c4...\" }\nfor app, expected in KNOWN_GOOD_HASHES:\n    if sha256(load_app(app)) != expected:\n        safe_mode()  // halt and alert ground\n\n// Also: enable secure boot, sign apps with HSM",
        "nist": "SI-7, SI-7(1), SI-7(6)",
        "cm": "CM0019, CM0020"
    },
    "REC-0005": {
        "title": "Eavesdropping",
        "how": "OBC implant monitored all CCSDS telecommands. Authentication enabled but encryption was NOT - all payloads in cleartext. 19 commands captured including propulsion sequences, ADCS parameters, life support setpoints, docking codes.",
        "fix": "// Enable AES-256-GCM encryption in CryptoLib\ncrypto_config->crypto_cipher = CRYPTO_CIPHER_AES256_GCM;\ncrypto_config->key_len = 32;\n// Upgrade CryptoLib to 1.4.2 (patches CVE-2025-29912)\n// Rotate symmetric keys each mission phase\n// Store keys in HSM only",
        "nist": "SC-8, SC-8(1), SC-28",
        "cm": "CM0007, CM0008"
    },
    "EXF-0001": {
        "title": "Downlink Exfiltration",
        "how": "Implant encoded command intelligence steganographically into housekeeping telemetry LSBs. Values within normal variance - no anomaly detection triggered. Full command vocabulary, propulsion sequences, Modbus register map exfiltrated over 60 days.",
        "fix": "# Detect steganographic exfiltration\nfrom scipy import stats\ndef detect_anomaly(frames, baseline):\n    lsb_values = [f & 0x01 for f in frames]\n    chi2, p_value = stats.chisquare(lsb_values)\n    if p_value < 0.05:\n        alert(\"Possible steganographic exfiltration\")",
        "nist": "SC-8, AU-12, SI-4",
        "cm": "CM0007, CM0044"
    },
    "EXF-0002": {
        "title": "RF Exfiltration",
        "how": "Implant transmitted real-time Haven-1 status via X-band science downlink disguised as Haven-1 Lab calibration data. Foreign asset received crew locations, hatch status, emergency system states during ground station handover gaps.",
        "fix": "# Sigma rule\ntitle: Haven-1 Unauthorized X-band Transmission\ndetection:\n    selection: { band: X-band, transmission_type: science_downlink }\n    filter: { scheduled_window: true }\n    condition: selection and not filter\nlevel: critical",
        "nist": "SC-8, SC-13, AU-12",
        "cm": "CM0007, CM0045"
    },
    "EX-0012.01": {
        "title": "Sensor Data Compromise",
        "how": "Using Modbus register addresses mapped during recon, implant wrote false life support values. O2 reported 20.9% while actual dropped to 14.2% below the 16% hypoxia threshold. No independent validation path. Crew experienced hypoxia while displays showed green.",
        "fix": "# Independent Modbus read bypassing OBC\nfrom pymodbus.client import ModbusTcpClient\nclient = ModbusTcpClient(LIFESUPPORT_IP)\nraw_o2 = client.read_holding_registers(0, 1).registers[0] / 10.0\ncfs_o2 = get_cfs_reported_o2()\nif abs(raw_o2 - cfs_o2) > 2.0:\n    alert_crew_and_ground(f\"O2 DISCREPANCY: raw={raw_o2}% reported={cfs_o2}%\")",
        "nist": "SI-4, SI-4(2), AU-12",
        "cm": "CM0041, CM0042"
    },
    "DE-0003": {
        "title": "On-Board Values Obfuscation",
        "how": "Implant intercepted all telemetry at cFS software bus before downlink. Life support values normalized. ADCS vectors falsified. Command counters manipulated. Vast ground ops received completely false picture. No independent telemetry path existed.",
        "fix": "# Ground physics model validates telemetry\ndef validate(reported, model):\n    expected = model.predict(reported.timestamp)\n    for metric in SAFETY_CRITICAL:\n        delta = abs(reported[metric] - expected[metric])\n        if delta > THRESHOLDS[metric]:\n            alert(metric, reported[metric], expected[metric])",
        "nist": "SI-4, AU-6",
        "cm": "CM0041, CM0043"
    },
    "EX-0001.01": {
        "title": "Command Replay",
        "how": "Attacker replayed captured propulsion sequences. CVE-2025-29912 bypassed replay counter. OBC accepted replayed commands as fresh. Station maneuvered over 72 hours via small burns during comm gaps. Downlink simultaneously disrupted.",
        "fix": "// Anti-replay - patch CryptoLib to 1.4.2\nbool validate_freshness(TC_t *frame) {\n    if (frame->sequence_counter <= last_valid_counter) {\n        log(\"REPLAY DETECTED\"); return false;\n    }\n    if ((now() - frame->timestamp) > 60) {\n        log(\"STALE COMMAND\"); return false;\n    }\n    last_valid_counter = frame->sequence_counter;\n    return true;\n}",
        "nist": "SC-8, SC-8(1)",
        "cm": "CM0007, CM0009"
    },
    "IMP-0002": {
        "title": "Safety - Mission Abort",
        "how": "Foreign asset achieved rendezvous after Haven-1 maneuvered to intercept trajectory. Implant commanded docking system to accept approach. Crew cognitively impaired from O2 spoofing. Physical emergency controls required crew action they could not perform. Station captured.",
        "fix": "CREW PHYSICAL CONTROLS (no software dependency):\n\nPROPULSION INHIBIT  Panel-A Row-3\n  Kills all thruster firing. No software override.\n\nCOMMS ISOLATION     Panel-B Row-1\n  Cuts all antenna feeds. Attacker C2 goes dark.\n\nOBC HARD RESET      Panel-C Emergency Row\n  Cold-boot from write-protected ROM. Wipes implant.\n\nINDEPENDENT BEACON  Panel-D Red Cover\n  Cannot be disabled via OBC command injection.",
        "nist": "CP-2, IR-4, PE-3",
        "cm": "CM0052, CM0053, CM0078"
    },
}


def build_heatmap(results, gap_report):
    executed = {}
    for step in results.get("steps", []):
        ttp_id = step.get("ttp_id", "")
        executed[ttp_id] = {
            "status": step.get("status", "unknown"),
            "crew_impact": step.get("crew_safety_impact", "none"),
            "step": step.get("step"),
            "name": step.get("name", "")
        }

    tactics = [
        {"id": "REC", "name": "Reconnaissance", "color": "#6366f1", "techniques": [
            {"id": "REC-0005",    "name": "Eavesdropping"},
            {"id": "REC-0005.01","name": "Uplink Intercept"},
            {"id": "REC-0005.02","name": "Downlink Intercept"},
            {"id": "REC-0008",   "name": "Gather Supply Chain Info"},
            {"id": "REC-0008.02","name": "Software Recon"},
        ]},
        {"id": "RD", "name": "Resource Development", "color": "#0ea5e9", "techniques": [
            {"id": "RD-0001",    "name": "Acquire Infrastructure"},
            {"id": "RD-0002",    "name": "Compromise Infrastructure"},
            {"id": "RD-0003",    "name": "Obtain Cyber Capabilities"},
            {"id": "RD-0003.02", "name": "Cryptographic Keys"},
        ]},
        {"id": "IA", "name": "Initial Access", "color": "#f59e0b", "techniques": [
            {"id": "IA-0001",    "name": "Compromise Supply Chain"},
            {"id": "IA-0001.02", "name": "Software Supply Chain"},
            {"id": "IA-0007",    "name": "Compromise Ground System"},
            {"id": "IA-0007.01", "name": "Compromise On-Orbit Update"},
            {"id": "IA-0008",    "name": "Rogue External Entity"},
            {"id": "IA-0009",    "name": "Trusted Relationship"},
            {"id": "IA-0009.02", "name": "Vendor"},
            {"id": "IA-0011",    "name": "Auxiliary Device Compromise"},
        ]},
        {"id": "EX", "name": "Execution", "color": "#ef4444", "techniques": [
            {"id": "EX-0001",    "name": "Replay"},
            {"id": "EX-0001.01", "name": "Command Packets"},
            {"id": "EX-0009",    "name": "Exploit Code Flaws"},
            {"id": "EX-0009.03", "name": "Known Vulnerability (COTS/FOSS)"},
            {"id": "EX-0010",    "name": "Malicious Code"},
            {"id": "EX-0010.03", "name": "Rootkit"},
            {"id": "EX-0012",    "name": "Modify On-Board Values"},
            {"id": "EX-0012.01", "name": "Registers (Sensor Spoof)"},
        ]},
        {"id": "PER", "name": "Persistence", "color": "#8b5cf6", "techniques": [
            {"id": "PER-0003",   "name": "Ground System Presence"},
            {"id": "PER-0005",   "name": "Credentialed Persistence"},
        ]},
        {"id": "DE", "name": "Defense Evasion", "color": "#06b6d4", "techniques": [
            {"id": "DE-0001",    "name": "Masquerading"},
            {"id": "DE-0002",    "name": "Defeat ALiveness Testing"},
            {"id": "DE-0003",    "name": "Modify Telemetry"},
            {"id": "DE-0004",    "name": "Modify Configuration Files"},
        ]},
        {"id": "LM", "name": "Lateral Movement", "color": "#10b981", "techniques": [
            {"id": "LM-0001",    "name": "Bus Pivot"},
            {"id": "LM-0002",    "name": "Flight Software Pivot"},
        ]},
        {"id": "EXF", "name": "Exfiltration", "color": "#f97316", "techniques": [
            {"id": "EXF-0001",   "name": "Downlink Data Exfil"},
            {"id": "EXF-0002",   "name": "RF Side Channel"},
            {"id": "EXF-0003",   "name": "Replay Exfiltration"},
        ]},
        {"id": "IMP", "name": "Impact", "color": "#dc2626", "techniques": [
            {"id": "IMP-0001",   "name": "Loss of Availability"},
            {"id": "IMP-0002",   "name": "Safety - Manipulate GNC"},
            {"id": "IMP-0003",   "name": "Denial of Control"},
            {"id": "IMP-0004",   "name": "Loss of Communication"},
            {"id": "IMP-0005",   "name": "Loss of Control"},
            {"id": "IMP-0006",   "name": "Manipulate Mission Data"},
        ]},
    ]

    def card(technique):
        tid = technique["id"]
        tname = technique["name"]
        if tid in executed and executed[tid]["status"] == "pass":
            info = executed[tid]
            crew = info["crew_impact"]
            crew_colors = {
                "critical": "#fca5a5", "high": "#fcd34d",
                "medium": "#86efac", "low": "#bfdbfe", "none": "#e5e7eb"
            }
            cc = crew_colors.get(crew, "#e5e7eb")
            return (
                "<div class=\"technique succeeded\">"
                "<div class=\"ttp-id\">" + tid + "</div>"
                "<div class=\"ttp-name\">" + tname + "</div>"
                "<div class=\"ttp-badge\">PASS - Step " + str(info["step"]) + "</div>"
                "<div class=\"crew-badge\" style=\"background:" + cc + ";color:#1f2937\">crew: " + crew + "</div>"
                "</div>"
            )
        elif tid in executed:
            return (
                "<div class=\"technique blocked\">"
                "<div class=\"ttp-id\">" + tid + "</div>"
                "<div class=\"ttp-name\">" + tname + "</div>"
                "<div class=\"ttp-badge\">BLOCKED</div>"
                "</div>"
            )
        else:
            return (
                "<div class=\"technique untested\">"
                "<div class=\"ttp-id\">" + tid + "</div>"
                "<div class=\"ttp-name\">" + tname + "</div>"
                "<div class=\"ttp-badge\">not tested</div>"
                "</div>"
            )

    tactic_cols = ""
    for tactic in tactics:
        cards = "".join(card(t) for t in tactic["techniques"])
        tactic_cols += (
            "<div class=\"tactic-col\">"
            "<div class=\"tactic-header\" style=\"background:" + tactic["color"] + "\">"
            + tactic["id"] + "<br><small>" + tactic["name"] + "</small>"
            "</div>"
            "<div class=\"techniques\">" + cards + "</div>"
            "</div>"
        )

    # Build detail sections for each executed technique
    detail_sections = ""
    for step in sorted(results.get("steps", []), key=lambda x: x["step"]):
        tid = step.get("ttp_id", "")
        rem = REMEDIATION.get(tid)
        if not rem:
            continue
        crew = step.get("crew_safety_impact", "none")
        crew_colors = {
            "critical": "#fca5a5", "high": "#fcd34d",
            "medium": "#86efac", "low": "#bfdbfe", "none": "#6b7280"
        }
        cc = crew_colors.get(crew, "#6b7280")
        detail_sections += (
            "<div class=\"finding-card\">"
            "<div class=\"finding-header\">"
            "<div class=\"finding-ttp\">" + tid + "</div>"
            "<div class=\"finding-title\">" + rem["title"] + "</div>"
            "<div class=\"finding-meta\">"
            "<span class=\"step-badge\">Step " + str(step["step"]) + "</span>"
            "<span class=\"crew-impact\" style=\"background:" + cc + ";color:#0f172a\">crew: " + crew + "</span>"
            "<span class=\"cm-badge\">CM: " + rem["cm"] + "</span>"
            "<span class=\"nist-badge\">NIST: " + rem["nist"] + "</span>"
            "</div>"
            "</div>"
            "<div class=\"finding-body\">"
            "<div class=\"finding-col\">"
            "<div class=\"col-label\">HOW THE ATTACK SUCCEEDED</div>"
            "<div class=\"col-text\">" + rem["how"] + "</div>"
            "</div>"
            "<div class=\"finding-col\">"
            "<div class=\"col-label\">REMEDIATION</div>"
            "<pre class=\"code-block\">" + rem["fix"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre>"
            "</div>"
            "</div>"
            "</div>"
        )

    passed = sum(1 for s in results.get("steps", []) if s["status"] == "pass")
    total = len(results.get("steps", []))
    gaps = gap_report.get("total_gaps_found", 0)
    top_cm = gap_report.get("top_countermeasure", "N/A")
    top_data = next(
        (c for c in gap_report.get("ranked_countermeasures", [])
         if c["cm_id"] == top_cm), {}
    )
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AEGIS - Haven-1 SPARTA Coverage Heatmap</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
       background: #0f172a; color: #e2e8f0; padding: 24px; }
.header { text-align: center; margin-bottom: 32px; }
.header h1 { font-size: 24px; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; }
.header p { color: #94a3b8; font-size: 14px; }
.stats { display: flex; gap: 16px; justify-content: center; margin-bottom: 24px; flex-wrap: wrap; }
.stat-card { background: #1e293b; border: 1px solid #334155; border-radius: 8px;
             padding: 16px 24px; text-align: center; min-width: 140px; }
.stat-value { font-size: 28px; font-weight: 700; }
.stat-label { font-size: 12px; color: #64748b; margin-top: 4px;
              text-transform: uppercase; letter-spacing: 0.05em; }
.legend { display: flex; gap: 16px; justify-content: center; margin-bottom: 24px; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #94a3b8; }
.legend-dot { width: 12px; height: 12px; border-radius: 2px; }
.matrix { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 16px; }
.tactic-col { min-width: 155px; flex: 1; }
.tactic-header { text-align: center; padding: 10px 6px; border-radius: 6px 6px 0 0;
                 font-size: 12px; font-weight: 700; color: #fff;
                 text-transform: uppercase; letter-spacing: 0.05em; }
.tactic-header small { font-weight: 400; font-size: 10px; text-transform: none; }
.techniques { display: flex; flex-direction: column; gap: 4px; margin-top: 4px; }
.technique { padding: 8px; border-radius: 4px; }
.technique.succeeded { background: #dc2626; border: 2px solid #991b1b; color: #fff; }
.technique.blocked { background: #16a34a; border: 1px solid #15803d; color: #fff; }
.technique.untested { background: #1e293b; border: 1px solid #334155; color: #475569; }
.ttp-id { font-size: 10px; font-weight: 700; opacity: 0.9; letter-spacing: 0.03em; }
.ttp-name { font-size: 11px; margin-top: 2px; line-height: 1.3; }
.ttp-badge { font-size: 9px; margin-top: 4px; opacity: 0.85;
             text-transform: uppercase; letter-spacing: 0.05em; }
.crew-badge { font-size: 9px; margin-top: 3px; padding: 1px 4px;
              border-radius: 3px; display: inline-block; font-weight: 600; }
.top-fix { background: #1e293b; border: 1px solid #334155;
           border-left: 4px solid #f59e0b; border-radius: 8px;
           padding: 20px 24px; margin-top: 32px; margin-bottom: 48px; }
.top-fix h3 { color: #f59e0b; font-size: 14px; text-transform: uppercase;
              letter-spacing: 0.05em; margin-bottom: 8px; }
.top-fix p { color: #cbd5e1; font-size: 14px; line-height: 1.6; }
.findings-header { text-align: center; margin: 48px 0 24px; }
.findings-header h2 { font-size: 20px; font-weight: 700; color: #f1f5f9; margin-bottom: 4px; }
.findings-header p { color: #64748b; font-size: 13px; }
.finding-card { background: #1e293b; border: 1px solid #334155; border-radius: 8px;
                margin-bottom: 16px; overflow: hidden; }
.finding-header { padding: 16px 20px; border-bottom: 1px solid #334155;
                  background: #162032; }
.finding-ttp { color: #ef4444; font-size: 11px; font-weight: 700;
               text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.finding-title { color: #f1f5f9; font-size: 16px; font-weight: 600; margin-bottom: 8px; }
.finding-meta { display: flex; gap: 8px; flex-wrap: wrap; }
.step-badge { background: #334155; color: #94a3b8; font-size: 11px;
              padding: 2px 8px; border-radius: 4px; }
.crew-impact { font-size: 11px; padding: 2px 8px; border-radius: 4px; font-weight: 600; }
.cm-badge { background: #1e3a5f; color: #60a5fa; font-size: 11px;
            padding: 2px 8px; border-radius: 4px; }
.nist-badge { background: #1a3a2a; color: #4ade80; font-size: 11px;
              padding: 2px 8px; border-radius: 4px; }
.finding-body { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.finding-col { padding: 20px; }
.finding-col:first-child { border-right: 1px solid #334155; }
.col-label { color: #64748b; font-size: 10px; text-transform: uppercase;
             letter-spacing: 0.08em; font-weight: 600; margin-bottom: 10px; }
.col-text { color: #cbd5e1; font-size: 13px; line-height: 1.7; }
.code-block { background: #0f172a; border: 1px solid #334155; border-radius: 6px;
              padding: 14px; font-family: "SF Mono", Monaco, monospace;
              font-size: 11px; color: #86efac; line-height: 1.6;
              overflow-x: auto; white-space: pre-wrap; word-break: break-word; }
.footer { text-align: center; margin-top: 48px; padding: 24px;
          color: #475569; font-size: 12px; border-top: 1px solid #1e293b; }
</style>
</head>
<body>

<div class="header">
  <h1>AEGIS - Haven-1 SPARTA Coverage Heatmap</h1>
  <p>Nation-State APT | Full Kill Chain Simulation | """ + ts + """</p>
</div>

<div class="stats">
  <div class="stat-card">
    <div class="stat-value" style="color:#ef4444">""" + str(passed) + "/" + str(total) + """</div>
    <div class="stat-label">Steps Passed</div>
  </div>
  <div class="stat-card">
    <div class="stat-value" style="color:#f59e0b">""" + str(gaps) + """</div>
    <div class="stat-label">Gaps Found</div>
  </div>
  <div class="stat-card">
    <div class="stat-value" style="color:#6366f1">""" + str(top_cm) + """</div>
    <div class="stat-label">Top Fix</div>
  </div>
  <div class="stat-card">
    <div class="stat-value" style="color:#10b981">""" + str(top_data.get("chains_blocked", 0)) + """</div>
    <div class="stat-label">Chains Blocked</div>
  </div>
</div>

<div class="legend">
  <div class="legend-item">
    <div class="legend-dot" style="background:#dc2626"></div>
    Technique succeeded
  </div>
  <div class="legend-item">
    <div class="legend-dot" style="background:#16a34a"></div>
    Blocked by existing control
  </div>
  <div class="legend-item">
    <div class="legend-dot" style="background:#1e293b;border:1px solid #334155"></div>
    Not tested in this scenario
  </div>
</div>

<div class="matrix">
""" + tactic_cols + """
</div>

<div class="top-fix">
  <h3>Top Priority Fix - """ + str(top_cm) + """</h3>
  <p>""" + str(top_data.get("description", "")) + """</p>
  <p style="margin-top:8px;color:#94a3b8;font-size:13px">
    Blocks """ + str(top_data.get("chains_blocked", 0)) + """ attack steps &nbsp;|&nbsp;
    Crew safety: """ + str(top_data.get("max_crew_safety_weight", 0)) + """/10
  </p>
</div>

<div class="findings-header">
  <h2>Attack Step Detail + Remediation</h2>
  <p>Every technique that succeeded — how it worked and the specific fix</p>
</div>

""" + detail_sections + """

<div class="footer">
  AEGIS - AI-Driven SPARTA Emulation &amp; Gap Identification System |
  Haven-1 Threat Model | SPARTA v3.2
</div>

</body>
</html>"""


if __name__ == "__main__":
    base = "/Users/music_lab/Documents/Security Engineer Portfolio/VAST Space/aegis"
    results_path = sys.argv[1] if len(sys.argv) > 1 else base + "/generated/results.json"
    gaps_path = sys.argv[2] if len(sys.argv) > 2 else base + "/generated/gap_report.json"
    output_path = base + "/generated/heatmap.html"

    print("[HEATMAP] Loading results...")
    results = load_json(results_path)
    print("[HEATMAP] Loading gap report...")
    gap_report = load_json(gaps_path)
    print("[HEATMAP] Rendering heatmap with detail sections...")
    html = build_heatmap(results, gap_report)
    with open(output_path, "w") as f:
        f.write(html)
    print("[HEATMAP] Saved to " + output_path)
    cmd = 'open "' + output_path + '"'
    os.system(cmd)
    print("[HEATMAP] Done")
