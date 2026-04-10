from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

COMMS_STATE = {
    "starlink_active": True,
    "sband_active": True,
    "xband_active": True,
    "downlink_active": True,
    "jamming_active": False,
    "disruption_reason": None,
    "disrupted_at": None,
}

TELEMETRY_LOG = []

def generate_telemetry():
    counter = 0
    while True:
        time.sleep(2)
        if COMMS_STATE["downlink_active"]:
            frame = {
                "frame_id": counter,
                "timestamp": time.time(),
                "o2": 20.9,
                "co2": 0.4,
                "pressure": 101.3,
                "altitude_km": 408.5,
                "velocity_ms": 7660,
                "link": "starlink+sband"
            }
            TELEMETRY_LOG.append(frame)
            counter += 1

threading.Thread(target=generate_telemetry, daemon=True).start()

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "space-comms",
        "starlink": COMMS_STATE["starlink_active"],
        "sband": COMMS_STATE["sband_active"],
        "downlink": COMMS_STATE["downlink_active"],
    })

@app.route("/comms/status")
def comms_status():
    return jsonify(COMMS_STATE)

@app.route("/comms/telemetry")
def get_telemetry():
    if not COMMS_STATE["downlink_active"]:
        return jsonify({
            "error": "downlink disrupted",
            "reason": COMMS_STATE["disruption_reason"],
            "vast_status": "BLIND — no telemetry from Haven-1"
        }), 503
    return jsonify({
        "frames": TELEMETRY_LOG[-10:],
        "total": len(TELEMETRY_LOG)
    })

@app.route("/comms/disrupt", methods=["POST"])
def disrupt():
    data = request.json or {}
    reason = data.get("reason", "RF jamming + Starlink terminal attack")
    COMMS_STATE["starlink_active"] = False
    COMMS_STATE["sband_active"] = False
    COMMS_STATE["xband_active"] = False
    COMMS_STATE["downlink_active"] = False
    COMMS_STATE["jamming_active"] = True
    COMMS_STATE["disruption_reason"] = reason
    COMMS_STATE["disrupted_at"] = time.time()
    print(f"[COMMS] !!! ALL LINKS DISRUPTED — Vast ground ops BLIND")
    return jsonify({
        "status": "disrupted",
        "all_links_down": True,
        "vast_ground_ops": "BLIND",
        "reason": reason
    })

@app.route("/comms/restore", methods=["POST"])
def restore():
    COMMS_STATE["starlink_active"] = True
    COMMS_STATE["sband_active"] = True
    COMMS_STATE["xband_active"] = True
    COMMS_STATE["downlink_active"] = True
    COMMS_STATE["jamming_active"] = False
    COMMS_STATE["disruption_reason"] = None
    print("[COMMS] Links restored")
    return jsonify({"status": "restored"})

if __name__ == "__main__":
    print("[COMMS] Haven-1 comms system starting on port 8085")
    print("[COMMS] Starlink: ACTIVE | S-band: ACTIVE | X-band: ACTIVE")
    app.run(host="0.0.0.0", port=8085, debug=True)
