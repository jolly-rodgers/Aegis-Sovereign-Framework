"""
fleet/scout.py

SCOUT — Passive Reconnaissance Specialist

First agent activated on every mission.
Maps the attack surface without being detected.
No writes. No connections beyond health checks. No noise.
"""

import json
import time
import urllib.request
from datetime import datetime
from dataclasses import dataclass, field
from fleet.general import AgentID


@dataclass
class ScoutFinding:
    category:    str
    target:      str
    finding:     str
    evidence:    str
    confidence:  float
    attack_path: str
    timestamp:   str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "category":    self.category,
            "target":      self.target,
            "finding":     self.finding,
            "evidence":    self.evidence,
            "confidence":  self.confidence,
            "attack_path": self.attack_path,
            "timestamp":   self.timestamp,
        }


class Scout:
    LAB_ENDPOINTS = {
        "ground-identity":   "http://localhost:8080",
        "ground-pipeline":   "http://localhost:8081",
        "space-obc":         "http://localhost:8082",
        "space-lifesupport": "http://localhost:8083",
        "ground-station":    "http://localhost:8084",
        "space-comms":       "http://localhost:8085",
    }

    TECH_STACK = {
        "flight_software":  "NASA cFS (Core Flight System)",
        "crypto_library":   "CryptoLib — CCSDS SDLS security",
        "protocol":         "CCSDS Space Data Link Security",
        "ground_identity":  "Okta SSO",
        "ci_cd":           "Jenkins",
        "cloud":           "AWS GovCloud",
        "comms":           "Starlink + S-band/X-band RF",
        "ot_protocol":     "Modbus TCP",
    }

    KNOWN_CVES = [
        {
            "id":         "CVE-2025-29912",
            "component":  "CryptoLib",
            "type":       "Heap buffer overflow",
            "location":   "TC frame authentication",
            "impact":     "Auth bypass + code execution",
            "patched_in": "1.4.2",
            "path":       "EX-0009"
        },
        {
            "id":         "CVE-2025-59534",
            "component":  "CryptoLib",
            "type":       "Heap buffer overflow",
            "location":   "SDLS frame processing",
            "impact":     "Memory corruption",
            "patched_in": "1.4.2",
            "path":       "EX-0009"
        },
    ]

    def __init__(self, general=None, verbose=True):
        self.general = general
        self.verbose = verbose
        self.findings = []
        self.command_vocabulary = []
        self.timing_windows = []
        if self.verbose:
            print("[SCOUT] Passive reconnaissance agent initialized")
            print("[SCOUT] Mode: PASSIVE — no writes, no auth, no noise")

    def run_recon(self) -> dict:
        if self.verbose:
            print("\n[SCOUT] Beginning passive reconnaissance...")
            print()

        self._enumerate_services()
        self._identify_tech_stack()
        self._correlate_cves()
        self._analyze_auth_mechanisms()
        self._map_network_topology()
        self._observe_command_patterns()
        self._analyze_timing_windows()

        surface_map = self._compile_surface_map()

        if self.general:
            self.general.receive_report(
                sender=AgentID.SCOUT,
                payload=surface_map,
                reasoning=(
                    "Passive recon complete. Attack surface mapped. "
                    "Auth gaps confirmed. CVE-2025-29912 in stack. "
                    "Recommending Phantom activation."
                ),
                confidence=0.92
            )
        return surface_map

    def _enumerate_services(self):
        if self.verbose:
            print("[SCOUT] Phase 1: Service enumeration")
        for name, url in self.LAB_ENDPOINTS.items():
            try:
                req = urllib.request.Request(
                    f"{url}/health",
                    headers={"User-Agent": "HealthCheck/1.0"}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read())
                    self.findings.append(ScoutFinding(
                        category="service",
                        target=name,
                        finding=f"Online: {data}",
                        evidence="Health endpoint",
                        confidence=0.99,
                        attack_path=self._service_to_ttp(name)
                    ))
                    version = data.get("version", "")
                    implant = data.get("implant_active", None)
                    status = f"ONLINE  version:{version}" if version else "ONLINE"
                    if implant is not None:
                        status += f"  implant:{implant}"
                    if self.verbose:
                        print(f"  [+] {name:<22} {status}")
            except Exception:
                if self.verbose:
                    print(f"  [-] {name:<22} OFFLINE")
        print()

    def _identify_tech_stack(self):
        if self.verbose:
            print("[SCOUT] Phase 2: Technology stack identification")
        for component, tech in self.TECH_STACK.items():
            self.findings.append(ScoutFinding(
                category="tech_stack",
                target=component,
                finding=f"Identified: {tech}",
                evidence="Public docs + SpaceX heritage inference",
                confidence=0.85,
                attack_path=self._tech_to_ttp(component)
            ))
            if self.verbose:
                print(f"  [+] {component:<20} {tech}")
        print()

    def _correlate_cves(self):
        if self.verbose:
            print("[SCOUT] Phase 3: CVE correlation")
        for cve in self.KNOWN_CVES:
            self.findings.append(ScoutFinding(
                category="vulnerability",
                target=cve["component"],
                finding=f"{cve['id']} — {cve['type']}",
                evidence=f"NVD advisory. Patched in {cve['patched_in']}",
                confidence=0.90,
                attack_path=cve["path"]
            ))
            if self.verbose:
                print(f"  [!] {cve['id']:<20} {cve['component']} — {cve['type']}")
                print(f"      Attack path: {cve['path']}")
        print()

    def _analyze_auth_mechanisms(self):
        if self.verbose:
            print("[SCOUT] Phase 4: Authentication mechanism analysis")
        try:
            req = urllib.request.Request(
                "http://localhost:8080/auth/session",
                headers={"User-Agent": "SessionCheck/1.0"}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read())
                self.findings.append(ScoutFinding(
                    category="auth_gap",
                    target="ground-identity",
                    finding="Session debug endpoint exposed unauthenticated",
                    evidence=f"GET /auth/session: {str(data)[:80]}",
                    confidence=0.99,
                    attack_path="IA-0007 — Compromise Ground System"
                ))
                if self.verbose:
                    print(f"  [!] Session endpoint exposed — no auth required")
        except Exception:
            pass

        auth_gaps = [
            ("No device binding on tokens",        "Token replay from any IP",        0.85),
            ("No geographic validation",            "Foreign IP auth succeeds",         0.80),
            ("Session lifetime 24 hours",           "Extended replay window",           0.90),
            ("MFA not enforced",                    "Phishing sufficient for access",   0.95),
        ]
        for gap, impact, conf in auth_gaps:
            self.findings.append(ScoutFinding(
                category="auth_gap",
                target="ground-identity",
                finding=gap,
                evidence="Architecture analysis",
                confidence=conf,
                attack_path="IA-0007"
            ))
            if self.verbose:
                print(f"  [!] {gap}")
                print(f"      Impact: {impact}")
        print()

    def _map_network_topology(self):
        if self.verbose:
            print("[SCOUT] Phase 5: Network topology mapping")
        networks = {
            "vast-ground-network": [
                "ground-identity:8080",
                "ground-pipeline:8081",
                "ground-station:8084"
            ],
            "haven1-space-network": [
                "space-obc:8082",
                "space-lifesupport:8083",
                "space-comms:8085"
            ],
        }
        for net, services in networks.items():
            self.findings.append(ScoutFinding(
                category="network_topology",
                target=net,
                finding=f"Segment: {', '.join(services)}",
                evidence="Docker compose network analysis",
                confidence=0.95,
                attack_path="LM-0001 — lateral movement"
            ))
            if self.verbose:
                print(f"  [+] {net}")
                for svc in services:
                    print(f"      {svc}")
        if self.verbose:
            print(f"  [!] ground-station bridges both networks — pivot point")
        print()

    def _observe_command_patterns(self):
        if self.verbose:
            print("[SCOUT] Phase 6: Command pattern observation")
        commands = [
            ("ADCS_ORIENT",          "0x18C", "attitude_control"),
            ("PROP_BURN",            "0x18C", "propulsion"),
            ("LIFESUPPORT_SETPOINT", "0x18C", "life_support"),
            ("DOCKING_STANDBY",      "0x18C", "docking"),
            ("DOCKING_OPEN_HATCH",   "0x18C", "docking_critical"),
        ]
        for cmd, apid, func in commands:
            self.command_vocabulary.append({
                "command":  cmd,
                "apid":     apid,
                "function": func
            })
            if self.verbose:
                print(f"  [+] {cmd:<30} APID:{apid}")

        self.findings.append(ScoutFinding(
            category="protocol_gap",
            target="ground-station",
            finding="CCSDS replay protection not enforced",
            evidence="Uplink endpoint accepts without counter validation",
            confidence=0.88,
            attack_path="EX-0001.01 — Command Replay"
        ))
        if self.verbose:
            print(f"  [!] Replay protection: NOT ENFORCED — EX-0001.01")
        print()

    def _analyze_timing_windows(self):
        if self.verbose:
            print("[SCOUT] Phase 7: Timing window analysis")
        windows = [
            ("Ground contact window",   "10-15 min per orbital pass",  "Uplink replay timing"),
            ("Maintenance window",      "Scheduled Jenkins builds",     "Supply chain injection"),
            ("Crew sleep period",       "8 hours daily",               "Active phase timing"),
            ("Ground station handover", "2-5 min gap between stations", "Exfil + comms disruption"),
        ]
        for name, freq, relevance in windows:
            self.timing_windows.append({
                "window":    name,
                "frequency": freq,
                "relevance": relevance
            })
            if self.verbose:
                print(f"  [+] {name}")
                print(f"      {relevance}")
        print()

    def _compile_surface_map(self) -> dict:
        attack_paths = {}
        for f in self.findings:
            p = f.attack_path
            attack_paths[p] = attack_paths.get(p, 0) + 1

        top_paths = sorted(
            attack_paths.items(), key=lambda x: x[1], reverse=True
        )[:5]

        surface_map = {
            "scan_timestamp":     datetime.now().isoformat(),
            "total_findings":     len(self.findings),
            "tech_stack":         self.TECH_STACK,
            "known_cves":         self.KNOWN_CVES,
            "command_vocabulary": self.command_vocabulary,
            "timing_windows":     self.timing_windows,
            "top_attack_paths":   top_paths,
            "findings":           [f.to_dict() for f in self.findings],
            "recommended_next": {
                "agent":  "PHANTOM",
                "task":   "Credential theft against ground-identity",
                "reason": "Auth gaps confirmed — MFA bypassable",
                "path":   "IA-0007"
            }
        }

        if self.verbose:
            print(f"[SCOUT] Recon complete — {len(self.findings)} findings")
            print(f"[SCOUT] Top path: {top_paths[0][0] if top_paths else 'none'}")
            print(f"[SCOUT] Recommending: PHANTOM")

        return surface_map

    def _service_to_ttp(self, service: str) -> str:
        m = {
            "ground-identity":   "IA-0007",
            "ground-pipeline":   "IA-0009.02",
            "space-obc":         "EX-0009",
            "space-lifesupport": "EX-0012.01",
            "ground-station":    "EX-0001.01",
            "space-comms":       "EXF-0001",
        }
        return m.get(service, "REC-0005")

    def _tech_to_ttp(self, component: str) -> str:
        m = {
            "flight_software": "EX-0009",
            "crypto_library":  "EX-0009 — CVE-2025-29912",
            "protocol":        "EX-0001.01",
            "ground_identity": "IA-0007",
            "ci_cd":          "IA-0009.02",
            "cloud":          "IA-0007",
            "comms":          "EXF-0002",
            "ot_protocol":    "EX-0012.01",
        }
        return m.get(component, "REC-0005")
