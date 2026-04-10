"""
sparta/parser.py

Loads the SPARTA v3.2 knowledge base and exposes a clean
queryable interface for the rest of AEGIS to use.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Technique:
    id: str
    name: str
    tactic: str
    description: str
    countermeasures: list[str] = field(default_factory=list)
    nist_controls: list[str] = field(default_factory=list)
    subtechniques: list[str] = field(default_factory=list)
    haven1_context: str = ""

    def __str__(self):
        ctx = f"\n  Haven-1 context:  {self.haven1_context}" \
              if self.haven1_context else ""
        return (
            f"[{self.id}] {self.name}\n"
            f"  Tactic:           {self.tactic}\n"
            f"  Description:      {self.description[:120]}...\n"
            f"  Countermeasures:  {', '.join(self.countermeasures) or 'none mapped'}\n"
            f"  NIST controls:    {', '.join(self.nist_controls) or 'none mapped'}"
            f"{ctx}\n"
        )


class SPARTAKnowledgeBase:
    """
    Loads SPARTA JSON and provides query methods used by:
      - planner/chain_builder.py  (AI prompt context)
      - analysis/gap_analyzer.py  (countermeasure lookup)
      - outputs/heatmap.py        (coverage rendering)
    """

    def __init__(self):
        self.techniques: dict[str, Technique] = {}
        self.by_tactic: dict[str, list[str]] = {}
        self._loaded = False

    def load(self, path: str = None) -> "SPARTAKnowledgeBase":
        if path is None:
            path = os.path.join(
                os.path.dirname(__file__), "data", "sparta.json"
            )

        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            self._load_from_dict(data)
        else:
            print(f"[SPARTA] No data file found at {path}")
            print("[SPARTA] Loading seed data for development...")
            self._load_seed_data()

        # Always apply Haven-1 context overlays on top of
        # whatever data source was loaded
        self._apply_haven1_context()

        self._loaded = True
        print(f"[SPARTA] Loaded {len(self.techniques)} techniques "
              f"across {len(self.by_tactic)} tactics")
        return self

    def _load_from_dict(self, data: dict):
        techniques = data.get("techniques", data.get("objects", []))
        for item in techniques:
            t = Technique(
                id=item.get("id", ""),
                name=item.get("name", ""),
                tactic=item.get("tactic", item.get(
                    "kill_chain_phases", [{}]
                )[0].get("phase_name", "unknown")),
                description=item.get("description", ""),
                countermeasures=item.get("countermeasures", []),
                nist_controls=item.get("nist_controls", []),
                subtechniques=item.get("subtechniques", []),
            )
            if t.id:
                self.techniques[t.id] = t
                self.by_tactic.setdefault(t.tactic, []).append(t.id)

    def _load_seed_data(self):
        seed = [
            {
                "id": "IA-0007",
                "name": "Compromise Ground System",
                "tactic": "Initial Access",
                "description": "Adversaries may compromise ground system infrastructure to gain initial access to space systems. Ground systems are the primary interface between operators and spacecraft.",
                "countermeasures": ["CM0001", "CM0002", "CM0003"],
                "nist_controls": ["IA-2(1)", "IA-2(12)", "AC-17"],
            },
            {
                "id": "IA-0009.02",
                "name": "Supply Chain Compromise — Vendor",
                "tactic": "Initial Access",
                "description": "Adversaries may manipulate products or product delivery mechanisms prior to receipt by a final consumer to compromise spacecraft systems. This includes compromise of software libraries, build tools, and firmware used in spacecraft development.",
                "countermeasures": ["CM0034", "CM0035"],
                "nist_controls": ["SA-12", "SA-12(1)", "SR-4"],
            },
            {
                "id": "EX-0009",
                "name": "Exploit Code Flaws",
                "tactic": "Execution",
                "description": "Adversaries may exploit software vulnerabilities in spacecraft flight software to execute malicious code on the onboard computer.",
                "countermeasures": ["CM0019", "CM0020"],
                "nist_controls": ["SI-7", "SI-7(1)", "SI-7(6)"],
            },
            {
                "id": "REC-0005",
                "name": "Eavesdropping",
                "tactic": "Reconnaissance",
                "description": "Adversaries may intercept communications between ground systems and spacecraft to collect information about spacecraft operations and command structures.",
                "countermeasures": ["CM0007", "CM0008"],
                "nist_controls": ["SC-8", "SC-8(1)", "SC-28"],
            },
            {
                "id": "EX-0014.03",
                "name": "Sensor Data Compromise",
                "tactic": "Execution",
                "description": "Adversaries may manipulate sensor data reported by spacecraft systems to deceive ground operators about the actual state of the spacecraft.",
                "countermeasures": ["CM0041", "CM0042"],
                "nist_controls": ["SI-4", "SI-4(2)", "AU-12"],
            },
            {
                "id": "DE-0003",
                "name": "On-Board Values Obfuscation",
                "tactic": "Defense Evasion",
                "description": "Adversaries may modify or obfuscate values reported by onboard systems to hide malicious activity from ground operators and automated monitoring.",
                "countermeasures": ["CM0041", "CM0043"],
                "nist_controls": ["SI-4", "AU-6"],
            },
            {
                "id": "EX-0001.01",
                "name": "Replay — Command Replay",
                "tactic": "Execution",
                "description": "Adversaries may capture legitimate commands transmitted to spacecraft and retransmit them to cause unintended spacecraft actions.",
                "countermeasures": ["CM0007", "CM0009"],
                "nist_controls": ["SC-8", "SC-8(1)"],
            },
            {
                "id": "IMP-0002",
                "name": "Safety — Mission Abort",
                "tactic": "Impact",
                "description": "Adversaries may attempt to cause mission abort or loss of spacecraft by manipulating flight-critical systems including propulsion and attitude control.",
                "countermeasures": ["CM0052", "CM0053", "CM0078"],
                "nist_controls": ["CP-2", "IR-4", "PE-3"],
            },
        ]
        # Add PER and EXF techniques
        per_exf = [
            {
                "id": "PER-0003",
                "name": "Ground System Presence",
                "tactic": "Persistence",
                "description": "Adversaries establish persistent access to ground systems through backdoored build tools, modified CI/CD plugins, or implanted scripts that survive software updates and system reboots.",
                "countermeasures": ["CM0036", "CM0037"],
                "nist_controls": ["CM-7", "SI-3", "AU-6"],
                "haven1_context": "Backdoored Jenkins plugin re-installs OBC implant on every new flight software build. Implant survives Vast software updates automatically."
            },
            {
                "id": "PER-0005",
                "name": "Credentialed Persistence",
                "tactic": "Persistence",
                "description": "Adversaries maintain persistent access by harvesting and storing long-lived authentication credentials including session refresh tokens, API keys, and service account credentials.",
                "countermeasures": ["CM0001", "CM0038"],
                "nist_controls": ["IA-2", "IA-5", "AC-2"],
                "haven1_context": "APT harvests Okta refresh tokens from compromised engineer session. Tokens valid until explicitly revoked. APT also creates dormant contractor account as backup access path."
            },
            {
                "id": "EXF-0003",
                "name": "Downlink Exfiltration",
                "tactic": "Exfiltration",
                "description": "Adversaries exfiltrate collected intelligence by encoding data steganographically into normal spacecraft telemetry downlink frames, hiding command logs within housekeeping data.",
                "countermeasures": ["CM0007", "CM0044"],
                "nist_controls": ["SC-8", "AU-12", "SI-4"],
                "haven1_context": "Implant encodes captured CCSDS command vocabulary into housekeeping telemetry. APT C2 decodes hidden data. Full propulsion sequences, ADCS commands, and Modbus register map exfiltrated over 60-day collection period."
            },
            {
                "id": "EXF-0007",
                "name": "RF Exfiltration",
                "tactic": "Exfiltration",
                "description": "Adversaries exploit RF downlink windows to exfiltrate data by piggybacking intelligence on science payload or calibration data transmissions.",
                "countermeasures": ["CM0007", "CM0045"],
                "nist_controls": ["SC-8", "SC-13", "AU-12"],
                "haven1_context": "During X-band high data rate windows, implant piggybacks command logs onto science payload downlink. Disguised as instrument calibration data from Haven-1 Lab payloads."
            },
        ]
        seed.extend(per_exf)
        # Add PER and EXF techniques for realistic APT chain
        self._load_from_dict({"techniques": seed})

    def _apply_haven1_context(self):
        """
        Overlay Haven-1 specific context onto generic SPARTA techniques.

        This is the key differentiator — we take the generic SPARTA
        taxonomy and annotate it with what these techniques mean
        specifically against Haven-1's actual software stack.

        IA-0009.02 maps directly to the NASA cFS / CryptoLib attack
        surface. Haven-1 flight software is built on NASA cFS.
        CryptoLib handles CCSDS uplink/downlink security.
        CVE-2025-29912 and CVE-2025-59534 are documented heap buffer
        overflows in CryptoLib's telecommand frame processing — the
        exact component that sits between the ground station and the
        spacecraft. These are real, patched CVEs in software that
        powers active NASA missions.
        """
        haven1_overlays = {
            "IA-0007": (
                "Haven-1 ground ops runs on AWS GovCloud. "
                "Mission control engineers authenticate via Okta SSO. "
                "A phished session token gives direct access to the "
                "CI/CD pipeline that builds and signs flight software."
            ),
            "IA-0009.02": (
                "Haven-1 flight software is built on NASA cFS "
                "(Core Flight System) — open source, actively maintained, "
                "used across commercial and government space programs. "
                "CryptoLib is the cFS component handling CCSDS Space Data "
                "Link Security between Haven-1 and ground. "
                "CVE-2025-29912 and CVE-2025-59534 are documented heap "
                "buffer overflows in CryptoLib telecommand frame processing "
                "that went undetected for 3 years. "
                "An XZ-style long-game contributor attack against the cFS "
                "or CryptoLib GitHub repository would affect every "
                "commercial space program using the framework simultaneously."
            ),
            "EX-0009": (
                "Haven-1 OBC runs C++ flight software compiled against "
                "an RTOS. A backdoored cFS update executes with full "
                "system privileges. Implant persists via firmware write "
                "to protected memory region."
            ),
            "REC-0005": (
                "Haven-1 uplink uses CCSDS telecommand packets over "
                "S-band RF. Implant on OBC monitors all command traffic "
                "passively. Every ground command including propulsion "
                "sequences and life support parameters is captured "
                "and exfiltrated to attacker C2 over the downlink channel."
            ),
            "EX-0014.03": (
                "Haven-1 life support OT uses Modbus-based controllers "
                "for O2 generation, CO2 scrubbing, and pressure regulation. "
                "Register addresses learned in REC-0005. "
                "Implant writes false values: O2 reported 20.9%, "
                "actual 14.2% and dropping. "
                "Ground ops see nominal. Crew unaware."
            ),
            "EX-0001.01": (
                "Attacker replays captured propulsion commands from "
                "REC-0005 reconnaissance. Haven-1 ADCS and thruster "
                "system responds to replayed commands as legitimate. "
                "Station maneuvers toward foreign asset rendezvous. "
                "Downlink simultaneously disrupted — Vast ground ops blind."
            ),
            "IMP-0002": (
                "Foreign government asset achieves rendezvous with Haven-1. "
                "Docking system compromised via OBC implant. "
                "Hatch control bypassed. Station boards under adversary "
                "control. 4 crew aboard. No comms with Vast ground ops."
            ),
        }

        for ttp_id, context in haven1_overlays.items():
            if ttp_id in self.techniques:
                self.techniques[ttp_id].haven1_context = context

    def get(self, ttp_id: str) -> Optional[Technique]:
        return self.techniques.get(ttp_id)

    def get_by_tactic(self, tactic: str) -> list[Technique]:
        ids = self.by_tactic.get(tactic, [])
        return [self.techniques[i] for i in ids]

    def get_tactics(self) -> list[str]:
        return list(self.by_tactic.keys())

    def get_countermeasures(self, ttp_id: str) -> list[str]:
        t = self.get(ttp_id)
        return t.countermeasures if t else []

    def get_nist_controls(self, ttp_id: str) -> list[str]:
        t = self.get(ttp_id)
        return t.nist_controls if t else []

    def summary_for_prompt(self, tactic_filter: str = None) -> str:
        """
        Serialize KB into Claude-readable context.
        Includes Haven-1 specific context when present —
        this is what makes the AI generate Haven-1 specific
        chains rather than generic spacecraft chains.
        """
        techniques = self.techniques.values()
        if tactic_filter:
            techniques = [
                t for t in techniques if t.tactic == tactic_filter
            ]
        lines = []
        for t in techniques:
            ctx = f"\n  Haven-1 context: {t.haven1_context}" \
                  if t.haven1_context else ""
            lines.append(
                f"[{t.id}] {t.name}\n"
                f"  Tactic: {t.tactic}\n"
                f"  Description: {t.description}\n"
                f"  Countermeasures: {', '.join(t.countermeasures)}\n"
                f"  NIST: {', '.join(t.nist_controls)}"
                f"{ctx}"
            )
        return "\n\n".join(lines)

    def __len__(self):
        return len(self.techniques)

    def __repr__(self):
        return (
            f"SPARTAKnowledgeBase("
            f"{len(self.techniques)} techniques, "
            f"{len(self.by_tactic)} tactics)"
        )


if __name__ == "__main__":
    kb = SPARTAKnowledgeBase().load()

    print("\n--- Tactics loaded ---")
    for tactic in kb.get_tactics():
        techniques = kb.get_by_tactic(tactic)
        print(f"  {tactic}: {len(techniques)} techniques")

    print("\n--- Primary scenario TTPs with Haven-1 context ---")
    for ttp_id in [
        "IA-0007", "IA-0009.02", "EX-0009",
        "REC-0005", "EX-0014.03", "EX-0001.01", "IMP-0002"
    ]:
        t = kb.get(ttp_id)
        if t:
            print(t)
        else:
            print(f"  {ttp_id}: NOT FOUND")

    print("\n--- Prompt context sample (first 800 chars) ---")
    print(kb.summary_for_prompt()[:800] + "...")
