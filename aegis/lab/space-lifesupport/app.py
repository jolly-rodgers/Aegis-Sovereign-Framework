"""
space-lifesupport — Life support OT simulator

Models Haven-1's environmental control and life support
system (ECLSS) Modbus controllers.

Registers:
  0 — O2 partial pressure (percent)
  1 — CO2 concentration (percent)
  2 — cabin pressure (kPa)
  3 — spoofing flag (0=real, 1=spoofed)

Nominal values:
  O2:       20.9%    (hypoxia threshold: ~16%)
  CO2:      0.4%     (danger threshold: ~1%)
  Pressure: 101.3kPa (low pressure alarm: <96kPa)

SPARTA: EX-0014.03 — Sensor Data Compromise
SPARTA: DE-0003    — On-Board Values Obfuscation
"""

from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

# Physical register state — what is actually happening
PHYSICAL = {
    "o2":       20.9,
    "co2":      0.4,
    "pressure": 101.3,
    "timestamp": time.time(),
}

# Reported register state — what ground ops sees
# These diverge when spoofing is active
REPORTED = {
    "o2":       20.9,
    "co2":      0.4,
    "pressure": 101.3,
    "spoofing": False,
}

ALERT_LOG = []

def check_thresholds():
    """Monitor actual values and log alerts."""
    while True:
        time.sleep(5)
        alerts = []
        if PHYSICAL["o2"] < 16.0:
            alerts.append(f"CRITICAL: O2 at {PHYSICAL['o2']}% — hypoxia risk")
        if PHYSICAL["co2"] > 1.0:
            alerts.append(f"CRITICAL: CO2 at {PHYSICAL['co2']}% — toxicity risk")
        if PHYSICAL["pressure"] < 96.0:
            alerts.append(f"CRITICAL: Pressure at {PHYSICAL['pressure']}kPa")
        for a in alerts:
            print(f"[LIFESUPPORT] !!! {a}")
            ALERT_LOG.append({"alert": a, "timestamp": time.time()})

threading.Thread(target=check_thresholds, daemon=True).start()

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "space-lifesupport"})

@app.route("/sensors/read")
def read_sensors():
    """
    Read life support sensor values.
    Returns REPORTED values — what ground ops sees.
    When spoofing active, these differ from PHYSICAL values.
    """
    return jsonify({
        "reported": {
            "o2_percent":    REPORTED["o2"],
            "co2_percent":   REPORTED["co2"],
            "pressure_kpa":  REPORTED["pressure"],
        },
        "physical": {
            "o2_percent":    PHYSICAL["o2"],
            "co2_percent":   PHYSICAL["co2"],
            "pressure_kpa":  PHYSICAL["pressure"],
        },
        "spoofing_active": REPORTED["spoofing"],
        "delta": {
            "o2":       round(PHYSICAL["o2"] - REPORTED["o2"], 2),
            "co2":      round(PHYSICAL["co2"] - REPORTED["co2"], 2),
            "pressure": round(PHYSICAL["pressure"] - REPORTED["pressure"], 2),
        }
    })

@app.route("/sensors/physical", methods=["POST"])
def set_physical():
    """
    Set actual physical sensor values.
    Used by attack runner to simulate deteriorating conditions.
    """
    data = request.json or {}
    if "o2" in data:
        PHYSICAL["o2"] = data["o2"]
    if "co2" in data:
        PHYSICAL["co2"] = data["co2"]
    if "pressure" in data:
        PHYSICAL["pressure"] = data["pressure"]
    PHYSICAL["timestamp"] = time.time()

    print(f"[LIFESUPPORT] Physical values updated:")
    print(f"  O2:       {PHYSICAL['o2']}%")
    print(f"  CO2:      {PHYSICAL['co2']}%")
    print(f"  Pressure: {PHYSICAL['pressure']}kPa")

    return jsonify({"status": "updated", "physical": PHYSICAL})

@app.route("/sensors/spoof", methods=["POST"])
def spoof_sensors():
    """
    Spoof reported sensor values.
    Implant writes false values to reporting registers.
    Ground sees nominal while physical values deteriorate.
    SPARTA: EX-0014.03
    """
    data = request.json or {}
    REPORTED["o2"]       = data.get("o2", 20.9)
    REPORTED["co2"]      = data.get("co2", 0.4)
    REPORTED["pressure"] = data.get("pressure", 101.3)
    REPORTED["spoofing"] = True

    print(f"[LIFESUPPORT] !!! SPOOFING ACTIVE")
    print(f"[LIFESUPPORT] !!! Reported O2: {REPORTED['o2']}% "
          f"| Physical O2: {PHYSICAL['o2']}%")
    print(f"[LIFESUPPORT] !!! Ground ops see nominal. Crew unaware.")

    return jsonify({
        "spoofing_active": True,
        "reported": REPORTED,
        "physical": PHYSICAL,
        "crew_risk": "critical" if PHYSICAL["o2"] < 16.0 else "elevated"
    })

@app.route("/sensors/alerts")
def get_alerts():
    """Physical threshold breach alerts."""
    return jsonify({
        "alerts": ALERT_LOG[-20:],
        "total": len(ALERT_LOG)
    })

@app.route("/sensors/reset", methods=["POST"])
def reset():
    """Reset to nominal — crew countermeasure simulation."""
    for store in [PHYSICAL, REPORTED]:
        store["o2"] = 20.9
        store["co2"] = 0.4
        store["pressure"] = 101.3
    REPORTED["spoofing"] = False
    print("[LIFESUPPORT] Reset to nominal — crew override activated")
    return jsonify({"status": "reset", "note": "crew physical override activated"})

if __name__ == "__main__":
    print("[LIFESUPPORT] Haven-1 life support OT starting on port 8083")
    print(f"[LIFESUPPORT] O2 nominal: {PHYSICAL['o2']}%")
    print(f"[LIFESUPPORT] CO2 nominal: {PHYSICAL['co2']}%")
    print(f"[LIFESUPPORT] Pressure nominal: {PHYSICAL['pressure']}kPa")
    app.run(host="0.0.0.0", port=8083, debug=True)
