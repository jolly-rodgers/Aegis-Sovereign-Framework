"""
ground-station — CCSDS telecommand endpoint simulator

Models Haven-1's uplink receiver — the endpoint that
accepts ground commands formatted as CCSDS packets.

Vast uses CCSDS because Haven-1 must interface with
SpaceX Dragon. Dragon Eye docking uses CCSDS.
All NASA CLD commercial crew programs require CCSDS.

Vulnerabilities:
  - No replay counter enforcement
  - Command authentication bypassable via CryptoLib vuln
  - Replayed commands accepted as fresh

SPARTA: REC-0005 — Eavesdropping
SPARTA: EX-0001.01 — Command Replay
"""

from flask import Flask, request, jsonify
import time
import hashlib

app = Flask(__name__)

# All commands received — captured by implant for replay
COMMAND_HISTORY = []
REPLAY_LOG = []

# Simulated CryptoLib auth — bypassed via CVE-2025-29912
# In the real world this would use CCSDS SDLS TC frame auth
CRYPTOLIB_PATCHED = False

def ccsds_auth_check(packet: dict) -> bool:
    """
    Simulate CryptoLib TC frame authentication.
    Vulnerability: CVE-2025-29912 heap buffer overflow
    allows bypassing this check with malformed frame header.
    """
    if not CRYPTOLIB_PATCHED:
        # Vulnerable — auth check can be bypassed
        # Malformed byte sequence in frame header skips validation
        if packet.get("bypass_auth", False):
            print("[UPLINK] !!! CryptoLib auth BYPASSED — CVE-2025-29912")
            return True
    # Normal auth check
    auth = packet.get("auth_token", "")
    return len(auth) > 0

def check_replay(packet: dict) -> bool:
    """
    Check if this is a replayed command.
    Vulnerability: counter not enforced — replay attacks succeed.
    """
    counter = packet.get("sequence_counter", 0)
    # Should reject if counter <= last seen counter
    # Vulnerability: we don't actually enforce this
    return True

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "ground-station",
        "cryptolib_patched": CRYPTOLIB_PATCHED,
        "commands_received": len(COMMAND_HISTORY),
    })

@app.route("/uplink/command", methods=["POST"])
def receive_command():
    """
    Receive and process a CCSDS telecommand packet.
    Logs all commands — implant captures these for REC-0005.
    """
    data = request.json or {}
    packet = {
        "sequence_counter": data.get("sequence_counter", 0),
        "apid":             data.get("apid", "0x18C"),
        "function_code":    data.get("function_code", "NOP"),
        "params":           data.get("params", {}),
        "auth_token":       data.get("auth_token", ""),
        "bypass_auth":      data.get("bypass_auth", False),
        "timestamp":        time.time(),
        "source":           data.get("source", "vast-ground-station"),
    }

    # Auth check — bypassable via CryptoLib vuln
    if not ccsds_auth_check(packet):
        return jsonify({"status": "rejected", "reason": "auth failed"}), 403

    # Replay check — not enforced (vulnerability)
    check_replay(packet)

    COMMAND_HISTORY.append(packet)

    print(f"[UPLINK] Command accepted: {packet['function_code']} "
          f"(seq: {packet['sequence_counter']}) "
          f"from {packet['source']}")

    return jsonify({
        "status": "accepted",
        "sequence_counter": packet["sequence_counter"],
        "function": packet["function_code"],
    })

@app.route("/uplink/history", methods=["GET"])
def get_history():
    """
    Full command history — implant exfiltrates this.
    Attacker maps complete control language from this endpoint.
    SPARTA: REC-0005 / EXF-0003
    """
    return jsonify({
        "commands": COMMAND_HISTORY,
        "total": len(COMMAND_HISTORY),
        "note": "complete uplink command history"
    })

@app.route("/uplink/replay", methods=["POST"])
def replay_command():
    """
    Replay a previously captured command.
    Attacker uses commands learned in REC-0005 to
    fire thrusters and maneuver the station.
    SPARTA: EX-0001.01 — Command Replay
    """
    data = request.json or {}
    original_seq = data.get("original_sequence_counter")

    # Find the original command
    original = next(
        (c for c in COMMAND_HISTORY
         if c["sequence_counter"] == original_seq),
        None
    )

    if not original:
        return jsonify({"error": "command not found in history"}), 404

    # Replay it with bypass
    replayed = {**original,
                "source": "attacker-c2",
                "bypass_auth": True,
                "replayed": True,
                "replay_timestamp": time.time()}

    COMMAND_HISTORY.append(replayed)
    REPLAY_LOG.append(replayed)

    print(f"[UPLINK] !!! COMMAND REPLAY: {replayed['function_code']}")
    print(f"[UPLINK] !!! Original seq {original_seq} replayed by attacker C2")
    print(f"[UPLINK] !!! CryptoLib auth bypassed via CVE-2025-29912")

    return jsonify({
        "status": "replayed",
        "function": replayed["function_code"],
        "warning": "replay attack successful — no counter enforcement"
    })

if __name__ == "__main__":
    print("[UPLINK] Haven-1 CCSDS uplink endpoint starting on port 8084")
    print(f"[UPLINK] CryptoLib patched: {CRYPTOLIB_PATCHED}")
    print("[UPLINK] WARNING: Replay counter not enforced")
    print("[UPLINK] WARNING: CryptoLib auth bypassable — CVE-2025-29912")
    app.run(host="0.0.0.0", port=8084, debug=True)
