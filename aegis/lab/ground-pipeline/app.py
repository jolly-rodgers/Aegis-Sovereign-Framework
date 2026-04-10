"""
ground-pipeline — Jenkins-style CI/CD pipeline simulator

Models Vast's flight software build and signing pipeline.
An authenticated engineer can trigger builds, inject
artifacts, and sign updates with the build key.

Real world: Haven-1 flight software is C++ built against
an RTOS. This pipeline compiles, signs, and packages
updates for uplink to the OBC.

Vulnerability: signing key stored in pipeline environment,
artifact integrity not verified before signing,
no SBOM validation, no OPA/Conftest gate.
SPARTA: IA-0009.02 — Supply Chain Compromise
"""

from flask import Flask, request, jsonify
import hashlib
import time
import os
import requests

app = Flask(__name__)
SSO_URL = os.environ.get("SSO_URL", "http://haven-sso:8080")

# Simulated signing key — stored in CI/CD env (vulnerability)
SIGNING_KEY = "vast-flight-sw-signing-key-2027-dev"
BUILD_LOG = []

def verify_token(token: str) -> dict | None:
    """Verify session token against SSO."""
    try:
        resp = requests.post(
            f"{SSO_URL}/auth/validate",
            json={"token": token},
            timeout=3
        )
        data = resp.json()
        return data.get("payload") if data.get("valid") else None
    except Exception:
        return None

def sign_artifact(artifact_name: str, content: str) -> str:
    """
    Sign a build artifact with the pipeline signing key.
    Vulnerability: no verification of artifact content before signing.
    Attacker with pipeline access can sign anything.
    """
    signature = hashlib.sha256(
        f"{SIGNING_KEY}:{artifact_name}:{content}".encode()
    ).hexdigest()
    return signature

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ground-pipeline"})

@app.route("/pipeline/builds", methods=["GET"])
def list_builds():
    """List recent build history."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not verify_token(token):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"builds": BUILD_LOG[-10:]})

@app.route("/pipeline/build", methods=["POST"])
def trigger_build():
    """
    Trigger a flight software build.
    Authenticated engineers can build and sign artifacts.
    Vulnerability: no artifact content inspection before signing.
    SPARTA: IA-0009.02
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        return jsonify({"error": "unauthorized"}), 401

    data = request.json or {}
    artifact_name = data.get("artifact", "haven1-fsw-update.bin")
    content = data.get("content", "legitimate-flight-software-payload")
    version = data.get("version", "1.0.0")

    signature = sign_artifact(artifact_name, content)

    build_record = {
        "build_id": f"build-{int(time.time())}",
        "artifact": artifact_name,
        "version": version,
        "content_hash": hashlib.md5(content.encode()).hexdigest(),
        "signature": signature,
        "signed_by": user.get("sub"),
        "clearance": user.get("clearance"),
        "timestamp": time.time(),
        "sbom_verified": False,
        "opa_policy_check": False,
        "content": content,
    }

    BUILD_LOG.append(build_record)

    print(f"[CICD] Build triggered by {user.get('sub')}")
    print(f"[CICD] Artifact: {artifact_name} v{version}")
    print(f"[CICD] Signature: {signature[:16]}...")
    print(f"[CICD] WARNING: No SBOM check. No OPA policy gate.")

    return jsonify({
        "status": "success",
        "build": build_record,
        "warning": "artifact signed without SBOM or OPA verification"
    })

@app.route("/pipeline/artifacts", methods=["GET"])
def list_artifacts():
    """List signed artifacts available for uplink."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not verify_token(token):
        return jsonify({"error": "unauthorized"}), 401
    artifacts = [
        {
            "artifact": b["artifact"],
            "version": b["version"],
            "signature": b["signature"],
            "signed_by": b["signed_by"],
        }
        for b in BUILD_LOG
    ]
    return jsonify({"artifacts": artifacts})

@app.route("/pipeline/signing-key", methods=["GET"])
def expose_key():
    """
    Debug endpoint that exposes the signing key.
    Vulnerability: never removed from prod.
    Attacker with valid token can extract the key
    and sign arbitrary artifacts.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    print(f"[CICD] WARNING: Signing key accessed by {user.get('sub')}")
    return jsonify({
        "signing_key": SIGNING_KEY,
        "warning": "this endpoint should not exist in production"
    })

if __name__ == "__main__":
    print("[CICD] Haven-1 flight software pipeline starting on port 8081")
    print("[CICD] Signing key loaded from environment")
    print("[CICD] WARNING: No SBOM validation configured")
    print("[CICD] WARNING: No OPA/Conftest policy gate")
    app.run(host="0.0.0.0", port=8081, debug=True)
