# GUARDIAN — Defensive Guardian
## Component 4 of SOVEREIGN

**Status:** Design Document — Year 2-3 Build Target

---

## 1. Mission

Build an AI-driven EDR specifically designed for Haven-1's
RTOS environment. Detect the exact memory corruption
vulnerabilities that CIPHER discovers. Autonomously
hot-patch the vulnerable binary in orbit without requiring
a system reboot. Four crew members cannot wait for a
maintenance window.

The core design principle:
```
Detect → Contain → Patch → Verify
Without rebooting.
Without ground intervention.
Without crew disruption.
In under 60 seconds.
```

---

## 2. Why Standard EDR Fails in Space

```
Standard EDR assumptions         Haven-1 reality
─────────────────────────────────────────────────────
Runs on Windows/Linux             Runs on RTOS
Can reboot to apply patches       Crew cannot survive reboot
Has network connectivity          Intermittent ground contact
Can phone home for signatures     8-20 minute signal delay
Has excess CPU/memory             Hard real-time constraints
Can pause processes               cFS apps cannot be paused
Has persistent storage            Limited protected storage
Updates signatures daily          Update window is monthly
```

GUARDIAN is built from scratch for this environment.
Every design decision accounts for RTOS constraints,
crew safety requirements, and orbital operations.

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       GUARDIAN                          │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              SENSOR LAYER                       │   │
│  │  Memory monitor  Process monitor  Comm monitor  │   │
│  │  Modbus watch    Command counter  Heap guard     │   │
│  └──────────────────────┬──────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────▼──────────────────────────┐   │
│  │           DETECTION ENGINE (AI)                 │   │
│  │  Physics model    Behavioral baseline           │   │
│  │  Anomaly scorer   Exploit signature matcher     │   │
│  │  CIPHER signature Confidence threshold          │   │
│  └──────────────────────┬──────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────▼──────────────────────────┐   │
│  │          RESPONSE ORCHESTRATOR                  │   │
│  │  Contain → Analyze → Patch → Verify             │   │
│  │  Human approval gate for flight-critical        │   │
│  └──────────────────────┬──────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────▼──────────────────────────┐   │
│  │           HOT-PATCH ENGINE                      │   │
│  │  Binary lift    Patch synthesis    Re-emit       │   │
│  │  HSM signing    OBC deployment    Verification  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Sensor Layer

### 4.1 Memory Monitoring

```
Heap guard implementation:
  Red zones around all heap allocations
  Canary values at allocation boundaries
  Write access monitoring on protected regions
  Stack overflow detection via guard pages

cFS specific monitoring:
  Software bus message buffer integrity
  cFS application heap usage tracking
  Protected memory region write attempts
  Firmware region modification attempts

Detection targets (from CIPHER research):
  Heap buffer overflow in CryptoLib
    Monitor: MAC verification buffer boundary
    Alert: Write beyond allocated heap block

  Integer overflow in frame length
    Monitor: TC frame length calculation
    Alert: Allocation size < requested write size

  Use-after-free in session management
    Monitor: Freed pointer dereference
    Alert: Access to freed memory region
```

### 4.2 Process Behavioral Monitoring

```
cFS application behavioral baseline:
  Normal CPU utilization per app (%)
  Normal memory growth rate per app
  Normal software bus message frequency
  Normal inter-app communication patterns

Anomaly detection:
  CPU spike in crypto_app > 2 sigma from baseline
    Possible: exploit execution consuming cycles

  New software bus route not in baseline
    Possible: implant hooking message bus

  Unexpected write to protected memory
    Possible: persistence mechanism

  Network connection from non-network app
    Possible: C2 establishment

RTOS constraint:
  Monitoring must consume < 2% CPU
  Cannot introduce jitter to hard real-time tasks
  Must run at lower priority than flight-critical
  Cannot block on any cFS resource
```

### 4.3 Communication Monitoring

```
Uplink command monitoring:
  Track sequence counter values
  Flag gaps or anomalies in sequence
  Alert on commands outside normal windows
  Detect replay (same counter seen twice)

Telemetry integrity monitoring:
  Physics model predicts expected values
  Compare predicted vs reported per frame
  Alert on divergence beyond threshold
  Specifically: O2 consumption rate model

Modbus gateway monitoring:
  All register reads and writes logged
  Rate limiting on write operations
  Alert on writes from unexpected sources
  Cross-validate with cFS reported values
```

---

## 5. Detection Engine

### 5.1 Physics-Based Anomaly Detection

```python
# Pseudocode — physics model for life support

class LifeSupportPhysicsModel:
    def __init__(self, crew_count, volume_m3):
        self.crew_count = crew_count        # 4
        self.volume = volume_m3             # 80 m3
        self.o2_consumption_per_person = 0.84  # kg/day

    def predict_o2_level(self, current_level, time_delta_hours):
        # O2 consumption is predictable
        consumption_rate = (
            self.o2_consumption_per_person *
            self.crew_count / 24  # per hour
        )
        # O2 generation is also measurable
        generation_rate = self.get_generation_rate()

        expected = (
            current_level +
            (generation_rate - consumption_rate) * time_delta_hours
        )
        return expected

    def validate(self, reported_level, time_delta_hours):
        expected = self.predict_o2_level(
            self.last_valid_level, time_delta_hours
        )
        delta = abs(reported_level - expected)

        # A sudden jump of 0.5% is physically impossible
        if delta > 0.5:
            return False, delta

        return True, delta

# This catches sensor spoofing even when
# the reported value is "plausible" in isolation
# because it's impossible given the rate of change
```

### 5.2 CIPHER Signature Integration

```
CIPHER provides Guardian with:
  Exact memory corruption pattern
  Heap layout at time of overflow
  Gadget addresses used in ROP chain
  Shellcode byte patterns
  cFS hook locations

Guardian uses these as:
  Memory pattern signatures
  Behavioral signatures (cFS bus hooking)
  Network pattern signatures (C2 beaconing)

Unlike traditional signature-based AV:
  Signatures are derived from mathematical proof
  Not from malware samples
  Not from CVE descriptions
  From the actual exploit that was proven
  to work against Haven-1's exact binary

Detection confidence:
  Pattern match on heap layout: 0.92
  Behavioral match on bus hook: 0.97
  Combined confidence: 0.999
  Threshold for autonomous response: 0.95
```

### 5.3 Confidence Scoring

```
Each detection event receives a confidence score:

Score < 0.70   Log and monitor
               No action taken
               Alert to security team next contact

Score 0.70-0.90 Isolate the affected subsystem
                Alert crew immediately
                Request ground authorization
                for remediation

Score 0.90-0.95 Isolate and contain automatically
                Hot-patch initiated pending approval
                Crew notified via audio/visual alert
                Ground notified at next contact

Score > 0.95    Autonomous response authorized
                Hot-patch deployed immediately
                Crew notified of automatic response
                Full forensic log preserved
                Ground report generated
```

---

## 6. Hot-Patch Engine

### 6.1 Why Hot-Patch (No Reboot)

```
The problem with traditional patching in orbit:

  System reboot takes: 45-90 seconds
  During reboot: no attitude control
  During reboot: no life support monitoring
  During reboot: no communication
  During reboot: crew is unprotected

  For Haven-1 specifically:
    4 crew aboard
    Life support depends on OBC
    ADCS depends on OBC
    Comms depends on OBC

  Rebooting the OBC to patch a vulnerability
  creates a 90-second window where the crew
  has no system protection at all.

  Hot-patching eliminates that window entirely.
```

### 6.2 Binary Lift-and-Repair Pipeline

```
Step 1: Binary acquisition
  GUARDIAN monitors the running binary
  Maintains known-good baseline hash
  Has copy of current deployed binary

Step 2: Lift to LLVM IR
  RetDec or McSema lifts ARM binary
  to LLVM Intermediate Representation
  IR is architecture-independent
  Can be analyzed and modified

Step 3: Vulnerability identification
  CIPHER provided the vulnerable code path
  GUARDIAN locates equivalent IR block
  Identifies the specific instruction
  causing the memory corruption

Step 4: Patch synthesis
  For heap buffer overflow:
    Add bounds check before memcpy
    Validate length against allocation size
    Return error if bounds exceeded

  For integer overflow:
    Add overflow check before arithmetic
    Use safe integer arithmetic functions

  For use-after-free:
    Add null check after free
    Clear pointer after free

Step 5: Patch verification
  Compile patched IR back to ARM
  Run CIPHER's crash input against patch
  Confirm crash no longer occurs
  Confirm normal operation preserved

Step 6: Deployment
  Sign patched binary with HSM key
  Deploy to running process via cFS
  hot-reload mechanism
  Verify process hash matches signed binary
  Log complete patch operation

Step 7: Confirmation
  Run CIPHER's PoC against patched system
  Confirm exploit no longer works
  Report to ground: patch successful
  Update baseline hash
```

### 6.3 Human Approval Gate

```
For flight-critical systems the human is in the loop:

  Automatic (score > 0.95):
    Non-flight-critical subsystems
    Ground segment components
    Payload systems
    Crew device network

  Human approval required (always):
    OBC flight software patches
    Life support control software
    Propulsion system software
    Attitude control software

  Human approval flow:
    1. GUARDIAN generates patch proposal
    2. Sends to crew display immediately
    3. Sends to ground at next contact
    4. Crew can approve from inside Haven-1
       Physical approval button on panel
    5. Ground can approve via uplink command
    6. Timeout (15 minutes): escalate to crew
    7. GUARDIAN deploys on approval

  Why crew can approve:
    Signal delay makes ground response slow
    Crew can physically verify system state
    Physical approval cannot be spoofed via OBC
    Crew safety is immediate — ground is 8 minutes away
```

---

## 7. Incident Response Integration

### 7.1 Forensic Preservation

```
When GUARDIAN detects an attack:

Immediate preservation (before any response):
  Memory snapshot of affected process
  Network capture of active connections
  cFS software bus message log
  Command counter history
  Telemetry history (actual vs reported)
  Heap layout at time of detection

Chain of custody:
  All forensic data cryptographically timestamped
  Hash of each artifact preserved
  Signed by GUARDIAN's forensic key
  Stored in protected memory region
  Transmitted to ground at next contact

Why this matters:
  Legal evidence for attribution
  Technical evidence for patch validation
  SPARTA technique confirmation
  Compliance documentation for CMMC 2.0
```

### 7.2 Crew Communication Protocol

```
When attack detected, crew receives:

Audio alert:
  "Security event detected. GUARDIAN responding."
  Crew does not need to take action initially.

Display message:
  ┌──────────────────────────────────────────┐
  │  GUARDIAN SECURITY ALERT                 │
  │                                          │
  │  Event:    Memory corruption detected    │
  │  System:   CryptoLib authentication     │
  │  Severity: HIGH                          │
  │  Status:   Patch ready for approval      │
  │                                          │
  │  Crew action required:                   │
  │  Press APPROVE to deploy patch           │
  │  Press DEFER to wait for ground contact  │
  │  Press ISOLATE for manual containment    │
  └──────────────────────────────────────────┘

Plain English — no jargon.
The crew are astronauts not security engineers.
GUARDIAN handles the technical response.
Crew makes the authorization decision.
```

---

## 8. Demo Sequence

```
5-minute GUARDIAN demonstration:

0:00  Show Haven-1 OBC running normally
      Normal telemetry. All systems nominal.
      "GUARDIAN is running in the background.
       Behavioral baseline established."

1:00  Run CIPHER's exploit against the OBC
      Memory corruption triggered
      Implant attempts to install

1:30  GUARDIAN detects the anomaly
      "Heap corruption detected in CryptoLib.
       Confidence: 0.97. Autonomous response
       authorized."

2:00  Show containment
      Affected process isolated
      No impact to life support or ADCS
      Crew display shows alert message

2:30  Show hot-patch pipeline
      Binary lifted to LLVM IR
      Patch synthesized in 8 seconds
      Patch compiled back to ARM

3:00  Show patch verification
      CIPHER's crash input runs against patch
      No crash. Patch confirmed valid.
      Signed with HSM key.

3:30  Show deployment
      Patch deployed to running process
      No reboot. cFS hot-reload.
      Process hash verified.

4:00  Show post-patch state
      Run CIPHER's exploit again
      No effect. Exploit blocked.
      Telemetry shows: normal operations throughout.

4:30  Show forensic report
      Complete incident timeline
      SPARTA technique mapping
      Compliance evidence generated
      Ready for ground review at next contact.

5:00  Questions

Key message:
  "From detection to patched in 90 seconds.
   No reboot. No crew disruption.
   The crew never knew there was an attack.
   GUARDIAN handled it autonomously."
```

---

## 9. Performance Requirements

```
Detection latency:     < 500ms from exploit trigger
Containment time:      < 2 seconds from detection
Patch synthesis:       < 30 seconds
Patch deployment:      < 60 seconds
Total response time:   < 90 seconds end to end

CPU overhead:          < 2% of OBC capacity
Memory overhead:       < 5% of available RAM
Storage requirement:   < 50MB for baseline + forensics

Real-time compliance:
  GUARDIAN runs at lowest cFS priority
  Cannot preempt flight-critical tasks
  Cannot introduce jitter to attitude control
  Cannot block on any shared resource
  Designed to fail safe — if GUARDIAN crashes
  it has zero impact on flight operations
```
