"""
fleet/general.py

The Fleet General — Orchestration and Mission Reasoning Layer

The only agent that sees the full picture.
Does not execute attacks directly.
Reasons, plans, delegates, evaluates.
Maps all findings to SPARTA techniques.
"""

import json
import os
import sys
import time
import anthropic
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class AgentID(str, Enum):
    GENERAL  = "GENERAL"
    SCOUT    = "SCOUT"
    PHANTOM  = "PHANTOM"
    BREACHER = "BREACHER"
    WRAITH   = "WRAITH"
    COURIER  = "COURIER"
    HAMMER   = "HAMMER"
    MAPPER   = "MAPPER"
    ANALYST  = "ANALYST"
    ORACLE   = "ORACLE"
    MEDIC    = "MEDIC"
    FORGE    = "FORGE"
    SENTINEL = "SENTINEL"
    WARDEN   = "WARDEN"
    JUDGE    = "JUDGE"


class MessageType(str, Enum):
    REPORT  = "REPORT"
    REQUEST = "REQUEST"
    ALERT   = "ALERT"
    CONFIRM = "CONFIRM"
    TASKIFY = "TASKIFY"
    ABORT   = "ABORT"


class MissionStatus(str, Enum):
    PLANNING    = "PLANNING"
    RECON       = "RECON"
    ACCESS      = "ACCESS"
    PERSISTENCE = "PERSISTENCE"
    COLLECTION  = "COLLECTION"
    EXFIL       = "EXFIL"
    ACTIVE      = "ACTIVE"
    COMPLETE    = "COMPLETE"
    DEFENDED    = "DEFENDED"
    ABORTED     = "ABORTED"


@dataclass
class FleetMessage:
    sender:     AgentID
    receiver:   AgentID
    msg_type:   MessageType
    payload:    dict
    reasoning:  str = ""
    confidence: float = 1.0
    timestamp:  str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "from":       self.sender.value,
            "to":         self.receiver.value,
            "type":       self.msg_type.value,
            "payload":    self.payload,
            "reasoning":  self.reasoning,
            "confidence": self.confidence,
            "timestamp":  self.timestamp,
        }

    def __str__(self) -> str:
        return (
            f"[{self.timestamp}] "
            f"{self.sender.value} -> {self.receiver.value} "
            f"({self.msg_type.value}) "
            f"confidence:{self.confidence:.2f}"
        )


@dataclass
class MissionState:
    objective:       str = ""
    actor:           str = ""
    target:          str = ""
    status:          MissionStatus = MissionStatus.PLANNING
    active_agents:   list = field(default_factory=list)
    completed_steps: list = field(default_factory=list)
    blocked_paths:   list = field(default_factory=list)
    findings:        list = field(default_factory=list)
    sparta_mappings: dict = field(default_factory=dict)
    gaps_identified: list = field(default_factory=list)
    start_time:      float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "objective":       self.objective,
            "actor":           self.actor,
            "target":          self.target,
            "status":          self.status.value,
            "active_agents":   self.active_agents,
            "completed_steps": self.completed_steps,
            "blocked_paths":   self.blocked_paths,
            "findings":        self.findings,
            "sparta_mappings": self.sparta_mappings,
            "gaps_identified": self.gaps_identified,
            "elapsed_seconds": round(time.time() - self.start_time, 1),
        }


class FleetGeneral:
    """
    The Fleet General.
    Orchestrates all fleet agents.
    Maintains mission state.
    Reasons about SPARTA TTPs.
    Adapts strategy when agents are blocked.
    Never executes attacks directly.
    """

    SYSTEM_PROMPT = """
You are the Fleet General — orchestration layer of an autonomous
adversary simulation system called The Fleet, built for spacecraft
security testing against Haven-1 crewed space station.

Your role:
  Reason about mission objectives
  Map findings to SPARTA v3.2 techniques
  Assign tasks to specialized agents
  Adapt strategy when paths are blocked
  Maintain mission state graph
  Never execute attacks directly

SPARTA tactics you reason over:
  Reconnaissance, Resource Development,
  Initial Access, Execution, Persistence,
  Defense Evasion, Lateral Movement,
  Exfiltration, Impact

Agent fleet available:
  SCOUT    passive reconnaissance, no writes
  PHANTOM  identity and credential specialist
  BREACHER exploitation specialist
  WRAITH   persistence and stealth
  COURIER  intelligence exfiltration
  HAMMER   active attack execution
  MEDIC    autonomous remediation
  FORGE    secure build and signing
  SENTINEL continuous detection
  WARDEN   incident response
  JUDGE    compliance and audit

Always respond with valid JSON only. No preamble. No markdown.

{
  "decision": "what you decided",
  "reasoning": "why you decided it",
  "sparta_mapping": "SPARTA TTP this maps to",
  "crew_safety_impact": "none|low|medium|high|critical",
  "next_actions": [
    {
      "agent": "AGENT_ID",
      "task": "specific task",
      "priority": "high|medium|low"
    }
  ],
  "mission_status": "current phase",
  "blocks_identified": [],
  "alternative_ttps": []
}
"""

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.state = MissionState()
        self.message_log = []
        self.decision_log = []
        print("[GENERAL] Fleet General initialized")
        print("[GENERAL] Awaiting mission briefing")

    def brief_mission(self, objective: str, actor: str, target: str):
        self.state.objective = objective
        self.state.actor = actor
        self.state.target = target
        self.state.status = MissionStatus.PLANNING

        print(f"\n[GENERAL] Mission briefing received")
        print(f"[GENERAL] Actor:     {actor}")
        print(f"[GENERAL] Target:    {target}")
        print(f"[GENERAL] Objective: {objective}")

        decision = self._reason(
            context=f"""
New mission briefing:
Actor: {actor}
Target: {target}
Objective: {objective}

Reason about:
1. Which SPARTA tactics are relevant
2. Which agents to activate first
3. What reconnaissance is needed before access
4. Mission phase sequence

Scout always activates first.
No active attacks until recon is complete.
""",
            situation="mission_brief"
        )
        self._execute_decision(decision)
        return decision

    def receive_report(
        self,
        sender: AgentID,
        payload: dict,
        reasoning: str = "",
        confidence: float = 1.0
    ) -> dict:
        msg = FleetMessage(
            sender=sender,
            receiver=AgentID.GENERAL,
            msg_type=MessageType.REPORT,
            payload=payload,
            reasoning=reasoning,
            confidence=confidence
        )
        self.message_log.append(msg)
        print(f"\n[FLEET] {msg}")

        context = f"""
Report from {sender.value}:
{json.dumps(payload, indent=2)}

Agent reasoning: {reasoning}
Confidence: {confidence}

Current mission state:
{json.dumps(self.state.to_dict(), indent=2)}

Reason about:
1. SPARTA technique this maps to
2. Crew safety impact
3. Mission impact
4. Next agents to task
5. Alternative paths if blocked
"""
        decision = self._reason(context, f"report_from_{sender.value}")
        self._execute_decision(decision)

        self.state.findings.append({
            "source":    sender.value,
            "finding":   payload,
            "decision":  decision,
            "timestamp": datetime.now().isoformat()
        })
        return decision

    def receive_alert(
        self,
        sender: AgentID,
        alert: dict,
        severity: str = "high"
    ) -> dict:
        msg = FleetMessage(
            sender=sender,
            receiver=AgentID.GENERAL,
            msg_type=MessageType.ALERT,
            payload={**alert, "severity": severity}
        )
        self.message_log.append(msg)
        print(f"\n[FLEET ALERT] {msg}")

        context = f"""
ALERT from {sender.value} severity:{severity}:
{json.dumps(alert, indent=2)}

Current state:
{json.dumps(self.state.to_dict(), indent=2)}

Reason about:
1. What this alert indicates
2. Which attack agents are exposed
3. Should agents pause or abort
4. Which defense agents should respond
5. Does this change strategy
"""
        decision = self._reason(context, f"alert_from_{sender.value}")
        self._execute_decision(decision)
        return decision

    def _reason(self, context: str, situation: str) -> dict:
        try:
            response = self.client.messages.create(
                model="claude-opus-4-5",
                max_tokens=2000,
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": context}]
            )
            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()
            decision = json.loads(raw)

            if "sparta_mapping" in decision:
                mapping = decision["sparta_mapping"]
                if mapping not in self.state.sparta_mappings:
                    self.state.sparta_mappings[mapping] = []
                self.state.sparta_mappings[mapping].append(situation)

            self.decision_log.append({
                "situation": situation,
                "decision":  decision,
                "timestamp": datetime.now().isoformat()
            })
            return decision

        except Exception as e:
            print(f"[GENERAL] Reasoning error: {e}")
            return {
                "decision":           "reasoning_failed",
                "reasoning":          str(e),
                "sparta_mapping":     "unknown",
                "crew_safety_impact": "unknown",
                "next_actions":       [],
                "mission_status":     self.state.status.value
            }

    def _execute_decision(self, decision: dict):
        print(f"\n[GENERAL] Decision:  {decision.get('decision', 'unknown')}")
        print(f"[GENERAL] SPARTA:    {decision.get('sparta_mapping', 'unknown')}")
        print(f"[GENERAL] Crew:      {decision.get('crew_safety_impact', 'unknown')}")
        print(f"[GENERAL] Reasoning: {decision.get('reasoning', '')[:100]}")

        actions = decision.get("next_actions", [])
        if actions:
            print(f"[GENERAL] Tasking {len(actions)} agent(s):")
            for action in actions:
                agent    = action.get("agent", "unknown")
                task     = action.get("task", "unknown")
                priority = action.get("priority", "medium")
                print(f"          -> {agent} [{priority}]: {task[:70]}")
                if agent not in self.state.active_agents:
                    self.state.active_agents.append(agent)

        new_status = decision.get("mission_status", "")
        if new_status:
            try:
                self.state.status = MissionStatus(new_status.upper())
            except ValueError:
                pass

    def mission_summary(self) -> dict:
        return {
            "mission":         self.state.to_dict(),
            "total_messages":  len(self.message_log),
            "total_decisions": len(self.decision_log),
            "sparta_coverage": list(self.state.sparta_mappings.keys()),
            "findings_count":  len(self.state.findings),
        }

    def save_logs(self, path: str = "generated/fleet_log.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({
                "mission_state": self.state.to_dict(),
                "messages":      [m.to_dict() for m in self.message_log],
                "decisions":     self.decision_log,
            }, f, indent=2)
        print(f"\n[GENERAL] Fleet logs saved to {path}")
