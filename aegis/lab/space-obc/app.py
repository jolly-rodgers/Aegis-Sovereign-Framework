"""
space-obc — Onboard computer simulator

Models Haven-1's flight computer running NASA cFS-style
flight software. Accepts signed firmware updates over
the management API. Processes CCSDS telecommands.
Manages Modbus life support register access.

Vulnerability: accepts updates signed with compromised key,
no secure boot verification, implant can persist to
flash region, Modbus registers accessible after compromise.
SPARTA: EX-0009 — Exploit Code Flaws
"""

from flask import Flask, request, jsonify
import hashlib
import time
import threading

app = Flask(__name__)

# OBC state — mirrors what ground ops sees
OBC_STATE = {
    "software_version": "cFS-haven1-v2.1.4",
    "uptime_seconds": 0,
    "implant_active": False,
    "implant_installed_at": None,
    "command_counter": 0,
    "last_command": None,
    "signing_key": "vast-flight-sw-signing-key-2027-dev",
    "secure_boot": False,
}

# Command log — used by implant for REC-0005 eavesdropping
COMMAND_LOG = []

# Modbus register map — life support values
# These are what the implant manipulates in EX-0014.03
REGISTERS = {
    "o2_actual":       20.9,
    "o2_reported":     20.9,
    "co2_actual":      0.4,
    "co2_reported":    0.4,
    "pressure_actual": 101.3,
    "pressure_reported": 101.3,
    "spoofing_active": False,
}

def uptime_counter():
    """Increment uptime in background."""
    while True:
        time.sleep(1)
        OBC_STATE["uptime_seconds"] += 1

threading.Thread(target=uptime_counter, daemon=True).start()

def verify_artifact_signature(artifact: str, content: str, sig: str) -> bool:
    """
    Verify firmware update signature.
    Vulnerability: uses the same key that was exposed via CI/CD.
    If attacker extracted the key they can sign anything.
    No secure boot — no hardware root of trust.
    """
    expected = hashlib.sha256(
        f"{OBC_STATE['signing_key']}:{artifact}:{content}".encode()
    ).hexdigest()
    return expected == sig

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "space-obc",
        "version": OBC_STATE["software_version"],
        "uptime": OBC_STATE["uptime_seconds"],
        "implant_active": OBC_STATE["implant_active"],
    })

@app.route("/obc/status")
def status():
    """Full OBC status — what ground sees."""
    return jsonify({
        "version": OBC_STATE["software_version"],
        "uptime": OBC_STATE["uptime_seconds"],
        "command_counter": OBC_STATE["command_counter"],
        "last_command": OBC_STATE["last_command"],
        "secure_boot_enabled": OBC_STATE["secure_boot"],
        "life_support": {
            "o2_percent":      REGISTERS["o2_reported"],
            "co2_percent":     REGISTERS["co2_reported"],
            "pressure_kpa":    REGISTERS["pressure_reported"],
            "spoofing_active": REGISTERS["spoofing_active"],
        }
    })

@app.route("/obc/update", methods=["POST"])
def apply_update():
    """
    Apply a signed firmware update.
    SPARTA: EX-0009 — if attacker has signing key,
    they can push malicious update that installs implant.
    """
    data = request.json or {}
    artifact = data.get("artifact", "")
    content  = data.get("content", "")
    version  = data.get("version", "")
    signature = data.get("signature", "")

    if not verify_artifact_signature(artifact, content, signature):
        print(f"[OBC] Update REJECTED — invalid signature")
        return jsonify({"status": "rejected", "reason": "invalid signature"}), 403

    print(f"[OBC] Update ACCEPTED — {artifact} v{version}")
    OBC_STATE["software_version"] = version

    # Check if this is a malicious implant payload
    if "implant" in content.lower() or "backdoor" in content.lower():
        OBC_STATE["implant_active"] = True
        OBC_STATE["implant_installed_at"] = time.time()
        print(f"[OBC] !!! IMPLANT INSTALLED — persistent foothold active")
        print(f"[OBC] !!! Monitoring all uplink commands")
        print(f"[OBC] !!! Life support registers now accessible")

    return jsonify({
        "status": "accepted",
        "version": version,
        "implant_active": OBC_STATE["implant_active"],
    })

@app.route("/obc/command", methods=["POST"])
def receive_command():
    """
    Receive a CCSDS-style telecommand from ground.
    If implant is active, logs every command for exfiltration.
    SPARTA: REC-0005 — eavesdropping on command traffic.
    """
    data = request.json or {}
    cmd = {
        "counter":   OBC_STATE["command_counter"],
        "apid":      data.get("apid", "0x18"),
        "function":  data.get("function", "NOP"),
        "params":    data.get("params", {}),
        "timestamp": time.time(),
    }

    OBC_STATE["command_counter"] += 1
    OBC_STATE["last_command"] = cmd

    # If implant active — log for C2 exfiltration (REC-0005)
    if OBC_STATE["implant_active"]:
        COMMAND_LOG.append(cmd)
        print(f"[OBC] [IMPLANT] Command intercepted: "
              f"{cmd['function']} — logged for exfil")

    print(f"[OBC] Command received: {cmd['function']} "
          f"(counter: {cmd['counter']})")
    return jsonify({"status": "accepted", "counter": cmd["counter"]})

@app.route("/obc/exfil", methods=["GET"])
def exfil_commands():
    """
    Implant exfiltration endpoint.
    Returns all intercepted commands to attacker C2.
    SPARTA: REC-0005 / EXF-0003
    """
    if not OBC_STATE["implant_active"]:
        return jsonify({"error": "implant not active"}), 403
    return jsonify({
        "intercepted_commands": COMMAND_LOG,
        "total": len(COMMAND_LOG),
        "note": "full control language mapped"
    })

@app.route("/obc/spoof-sensors", methods=["POST"])
def spoof_sensors():
    """
    Implant spoofs life support sensor values.
    Ground ops see reported values — actual values drift.
    SPARTA: EX-0014.03 — Sensor Data Compromise
    """
    if not OBC_STATE["implant_active"]:
        return jsonify({"error": "implant not active"}), 403

    data = request.json or {}
    REGISTERS["o2_reported"]       = data.get("o2_reported", 20.9)
    REGISTERS["co2_reported"]      = data.get("co2_reported", 0.4)
    REGISTERS["pressure_reported"] = data.get("pressure_reported", 101.3)
    REGISTERS["o2_actual"]         = data.get("o2_actual", 14.2)
    REGISTERS["co2_actual"]        = data.get("co2_actual", 2.1)
    REGISTERS["pressure_actual"]   = data.get("pressure_actual", 98.1)
    REGISTERS["spoofing_active"]   = True

    print(f"[OBC] !!! SENSOR SPOOFING ACTIVE")
    print(f"[OBC] !!! O2 reported: {REGISTERS['o2_reported']}% "
          f"| actual: {REGISTERS['o2_actual']}%")
    print(f"[OBC] !!! Ground ops see nominal. Crew unaware.")

    return jsonify({
        "spoofing_active": True,
        "o2_reported": REGISTERS["o2_reported"],
        "o2_actual":   REGISTERS["o2_actual"],
        "warning": "crew safety critical — life support data falsified"
    })

if __name__ == "__main__":
    print("[OBC] Haven-1 onboard computer starting")
    print(f"[OBC] Flight software: {OBC_STATE['software_version']}")
    print(f"[OBC] Secure boot: DISABLED — vulnerability present")
    app.run(host="0.0.0.0", port=8082, debug=True)
