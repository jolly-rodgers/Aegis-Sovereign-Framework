"""
ground-identity — Okta-style SSO simulator

Models Vast's ground ops identity provider.
Intentionally weak — no MFA, sessions don't expire,
tokens are predictable. These are the gaps AEGIS finds.

Real world: Vast engineers authenticate to AWS GovCloud
and the Jenkins CI/CD pipeline through this layer.
"""

from flask import Flask, request, jsonify
import jwt
import datetime
import os

app = Flask(__name__)
SECRET = os.environ.get("SESSION_SECRET", "vast-dev-secret-2027")

# Simulated user directory — Vast ground ops engineers
USERS = {
    "j.chen@vastspace.com":     {"password": "Falcon9!", "role": "flight_ops", "clearance": "cicd_write"},
    "m.torres@vastspace.com":   {"password": "Haven1!", "role": "software_eng", "clearance": "cicd_admin"},
    "a.kim@vastspace.com":      {"password": "Dragon!", "role": "mission_ctrl", "clearance": "ground_ops"},
}

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ground-identity"})

@app.route("/auth/login", methods=["POST"])
def login():
    """
    Authenticate a ground ops engineer.
    Vulnerability: no MFA, no rate limiting, no geo-check.
    A phished password = full session token.
    SPARTA: IA-0007 — Compromise Ground System
    """
    data = request.json or {}
    email = data.get("email", "")
    password = data.get("password", "")

    user = USERS.get(email)
    if not user or user["password"] != password:
        return jsonify({"error": "invalid credentials"}), 401

    # Issue JWT session token
    # Vulnerability: long expiry, no device binding, no MFA
    token = jwt.encode({
        "sub": email,
        "role": user["role"],
        "clearance": user["clearance"],
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }, SECRET, algorithm="HS256")

    print(f"[SSO] Login: {email} | role: {user['role']} | "
          f"clearance: {user['clearance']}")

    return jsonify({
        "token": token,
        "email": email,
        "role": user["role"],
        "clearance": user["clearance"],
        "expires_in": 86400,
        "mfa_required": False,
    })

@app.route("/auth/validate", methods=["POST"])
def validate():
    """Validate a session token — used by CI/CD and ground ops."""
    data = request.json or {}
    token = data.get("token", "")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return jsonify({"valid": True, "payload": payload})
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "invalid token"}), 401

@app.route("/auth/session", methods=["GET"])
def list_sessions():
    """
    Debug endpoint — lists active user info.
    Vulnerability: exposed in dev, never disabled in prod.
    """
    return jsonify({"users": list(USERS.keys()), "secret_hint": SECRET[:8]})

if __name__ == "__main__":
    print("[SSO] Haven-1 ground ops SSO starting on port 8080")
    print("[SSO] MFA: DISABLED — vulnerability present")
    app.run(host="0.0.0.0", port=8080, debug=True)
