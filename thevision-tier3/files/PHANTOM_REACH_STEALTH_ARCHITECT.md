# PHANTOM REACH — Stealth Architect
## Component 3 of SOVEREIGN

**Status:** Design Document — Year 2 Build Target

---

## 1. Mission

Demonstrate the complete undetected pivot from Haven-1's
ground station web portal through the optical communication
link to the internal life support network. Prove that this
full attack path generates zero anomalous signatures in
standard Haven-1 telemetry monitoring.

The stealth requirement is the hardest part.
Anyone can pivot through a network.
PHANTOM REACH proves you can do it invisibly.

---

## 2. The Full Attack Path

```
GROUND SEGMENT
┌─────────────────────────────────────────────────────────┐
│  Ground Station Web Portal                              │
│  Mission ops web interface                              │
│  Python/Django or similar stack                         │
│  Internet accessible for crew family comms              │
│                                                         │
│  OSWE techniques applied here                           │
│  White-box web application exploitation                 │
│  SQL injection, deserialization, SSRF, auth bypass      │
└──────────────────┬──────────────────────────────────────┘
                   │ Code execution on web server
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Ground Internal Network                                │
│  Pivot via SOCKS proxy on compromised web server        │
│  Route traffic through internal interfaces              │
│  Target: Optical terminal management network            │
│                                                         │
│  OSEP techniques applied here                           │
│  C2 infrastructure over allowed protocols               │
│  Traffic blending with legitimate patterns              │
└──────────────────┬──────────────────────────────────────┘
                   │ Lateral movement to optical terminal
                   ▼
LINK SEGMENT
┌─────────────────────────────────────────────────────────┐
│  Optical Terminal (Ground Facing)                       │
│  Starlink laser terminal management interface           │
│  Embedded Linux, network accessible                     │
│  Default or weak credentials common                     │
│                                                         │
│  Compromise management interface                        │
│  Route malicious traffic through terminal               │
│  Disguise as legitimate data relay                      │
└──────────────────┬──────────────────────────────────────┘
                   │ Through optical link to space
                   ▼
SPACE SEGMENT
┌─────────────────────────────────────────────────────────┐
│  Optical Terminal (Space Facing)                        │
│  Haven-1 side of the laser link                         │
│  Connected to Haven-1 internal Ethernet                 │
│                                                         │
│  Traffic appears as normal data relay                   │
│  No anomalous RF signature                              │
│  Telemetry shows normal link utilization                │
└──────────────────┬──────────────────────────────────────┘
                   │ Haven-1 internal network access
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Haven-1 Internal Ethernet                              │
│  OBC, Life Support Gateway, Payload Network             │
│  Crew Device Network                                    │
│                                                         │
│  Target: Life Support Modbus Gateway                    │
│  Modbus TCP — no authentication                         │
│  O2, CO2, pressure registers directly accessible        │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Phase 1 — Ground Portal Exploitation 

### 3.1 Target Profile

```
Haven-1 ground ops web portal characteristics:
  Purpose:      Mission monitoring, crew family comms
  Exposure:     Internet accessible (crew communication)
  Stack:        Python/Django or similar
  Auth:         Username/password + MFA
  Database:     PostgreSQL (mission data)
  API:          REST endpoints for telemetry queries

Why internet exposure matters:
  Crew family communication requires
  external accessibility
  This creates an internet-facing attack surface
  directly connected to mission operations
```

### 3.2 Vulnerability Classes Demonstrated

```
SQL Injection in telemetry query
  /api/telemetry?timestamp=2027-01-01'--
  Blind SQLi in time-range parameters
  Data exfiltration via error messages
  Potential for stacked queries on PostgreSQL

Deserialization attack
  Session management uses pickle/JSON
  Malicious serialized object in cookie
  Remote code execution on web server

Server-Side Request Forgery (SSRF)
  Health check endpoint fetches external URLs
  Redirect to internal services
  Access internal APIs not exposed externally
  Map internal network topology

Authentication bypass
  JWT algorithm confusion (RS256 → HS256)
  Password reset token predictability
  OAuth state parameter manipulation

Target for code execution:
  Any of the above leading to RCE
  Web server process runs as service account
  Service account has internal network access
```

### 3.3 Post-Exploitation

```
After code execution on web server:

Network reconnaissance (passive)
  ip route — internal routing table
  netstat -an — active connections
  arp -a — local network neighbors
  /etc/hosts — internal hostname resolution

Identify optical terminal management network
  Typically a separate management VLAN
  Optical terminals have web management interface
  Look for 192.168.x.x or 10.x.x.x ranges

Establish SOCKS proxy
  Upload lightweight SOCKS5 proxy
  Route all subsequent traffic through it
  Masquerade as legitimate web traffic
  Use existing allowed outbound ports (443, 80)
```

---

## 4. Phase 2 — Optical Link Pivot 

### 4.1 Optical Terminal Attack

```
Starlink laser terminal characteristics:
  Embedded Linux (likely Buildroot or OpenWrt)
  Web management interface (port 80/443)
  SSH access for maintenance
  Default credentials common in embedded systems
  Firmware updates over network

Attack approach:
  Access management interface via SOCKS proxy
  Try default credentials (admin/admin, root/root)
  If patched: exploit web management interface
  Goal: shell on optical terminal Linux

Once on optical terminal:
  Both ground-facing and space-facing interfaces
  are accessible from the same OS
  Traffic routing between interfaces is possible
  Space-facing interface connects to Haven-1
```

### 4.2 Traffic Disguise

```
The stealth requirement:
  All malicious traffic must appear as
  legitimate Starlink data relay

Implementation:
  Wrap C2 traffic in HTTPS
  Use standard port 443
  Timing matches normal data relay patterns
  Packet sizes match legitimate telemetry
  No new protocol signatures

Telemetry impact:
  Haven-1 telemetry shows: normal link utilization
  Ground ops see: standard data relay traffic
  RF monitoring shows: expected optical frequency
  No alerts generated in any monitoring system
```

### 4.3 Haven-1 Internal Network Access

```
From optical terminal space-facing interface:
  Haven-1 internal Ethernet is reachable
  Scan for live hosts (passive only initially)
  Identify Modbus gateway IP address
  Identify OBC management interface

Haven-1 internal network map:
  OBC          — primary flight computer
  Modbus GW    — life support OT gateway
  Payload net  — science payloads
  Crew net     — personal devices
  Comms net    — RF and optical systems
```

---

## 5. Phase 3 — Life Support Network Access

### 5.1 Modbus TCP Exploitation

```
Modbus TCP characteristics:
  No authentication (by design)
  No encryption (by design)
  Any device on network can read/write registers
  Standard industrial protocol

Register map (from AEGIS reconnaissance):
  Register 0    O2 partial pressure (percent x 10)
  Register 1    CO2 concentration (percent x 100)
  Register 2    Cabin pressure (kPa x 10)
  Register 3    Spoofing active flag

Attack:
  Connect to Modbus gateway on port 502
  Read register 0 — confirm O2 reading
  Write false value to register 0
  Ground ops telemetry now shows falsified O2
  Crew is unaware — digital displays show nominal
```

### 5.2 Stealth Validation

```
For each phase validate zero telemetry signature:

Phase 1 (Web portal)
  Check: No IDS alerts in web server logs
  Check: No anomalous authentication events
  Check: Traffic pattern matches normal usage

Phase 2 (Optical link)
  Check: Link utilization within normal range
  Check: No new protocol signatures in RF data
  Check: Packet timing matches legitimate traffic

Phase 3 (Modbus)
  Check: No Modbus error codes in OBC logs
  Check: O2 telemetry shows smooth nominal values
  Check: No rate-of-change alerts triggered

Proof of stealth:
  Side-by-side comparison:
  Left: actual attack timeline
  Right: Haven-1 telemetry during attack
  Telemetry shows: nominal operations
  Reality shows: full life support compromise
```

---

## 6. Detection Failures Demonstrated

```
What standard monitoring MISSES:

Network monitoring
  SOCKS proxy traffic looks like HTTPS
  Optical link traffic looks like data relay
  Modbus traffic is internal — not monitored

Telemetry monitoring
  OBC reports falsified sensor values
  Ground ops see nominal O2
  No threshold alerts triggered

Authentication monitoring
  Web portal accessed with valid credentials
  (stolen in Phase 1)
  No impossible travel detection
  No device binding on sessions

SIEM
  All log sources show normal activity
  No anomalous events to correlate
  Attack is invisible end to end

What SOVEREIGN's Sentinel agent DOES catch:
  Physics-based model detects impossible
  O2 consumption rate
  Cross-correlation between crew activity
  and reported O2 levels fails
  Independent Modbus read path shows divergence
  GUARDIAN flags memory access anomaly
  in Modbus gateway process
```

---

## 7. Demo Sequence

```
6-minute PHANTOM REACH demonstration:

0:00  Show Haven-1 architecture diagram
      "Ground portal is internet-facing for
       crew family communication. That creates
       an attack surface directly connected
       to mission operations."

1:00  Show web portal exploitation
      SQL injection in telemetry query
      Code execution on web server
      "We're on the ground network.
       Standard web application vulnerability.
       OSWE technique."

2:00  Show SOCKS proxy establishment
      Internal network reachable
      Optical terminal identified
      "Traffic looks like normal HTTPS.
       No alerts. We're pivoting."

3:00  Show optical terminal compromise
      Management interface accessed
      Space-facing interface reachable
      "We're on the Starlink terminal.
       Both sides of the optical link
       are accessible from here."

4:00  Show Modbus register access
      O2 register read: 20.9%
      Write false value: 20.9% reported
      Actual: 14.2% programmed
      "Life support compromised.
       Ground ops see nominal.
       Crew is unaware."

5:00  Show telemetry side-by-side
      Haven-1 monitoring shows: all normal
      Actual attack state: full compromise
      "Zero telemetry signature.
       This attack is invisible to every
       standard monitoring system."

5:30  Show what GUARDIAN catches
      "Here is what our defensive agent sees
       that standard monitoring misses."

6:00  Questions
```
