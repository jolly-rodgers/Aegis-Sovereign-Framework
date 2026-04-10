# CIPHER — Binary Specialist
## Component 1 of SOVEREIGN

**Status:** Design Document — Year 1-2 Build Target

---

## 1. Mission

Discover real vulnerabilities in CCSDS protocol parsers
and flight control binaries. Prove exploitability from
first principles using mathematical constraint solving.
Feed confirmed working exploits to The Fleet General
for simulation against Haven-1.

The difference between AEGIS and CIPHER:

```
AEGIS    References CVE-2025-29912
CIPHER   Proves CVE-2025-29912 is exploitable against
         Haven-1's exact binary with a working ROP chain
         validated by Z3 constraint satisfaction
```

That is the difference between a security assessment
and a security proof.

---

## 2. Target Architecture

```
Primary target:
  NASA cFS (Core Flight System)
  Compiled for ARM Cortex-A series
  Same instruction set as flight hardware
  Running on RTOS (VxWorks or RTEMS class)

Specific attack surface:
  CryptoLib TC frame authentication
  CCSDS Space Data Link Security (SDLS) parser
  Telecommand frame length field processing
  Authentication field boundary conditions

Why this target:
  CryptoLib is open source on GitHub
  CVE-2025-29912 is documented
  TC frame parsing is the ground-to-space
  communication entry point
  Code execution here = full OBC control
```

---

## 3. Technical Stack

```
Fuzzing
  AFL++             feedback-driven greybox fuzzer
  LLVM              instrumentation for coverage
  CmpLog            comparison coverage for magic bytes
  libFuzzer         alternative for unit-level fuzzing

Static Analysis
  angr              binary analysis framework
  Control flow graph generation
  Dangerous function identification
  Seed corpus generation from static paths

Constraint Solving
  Z3 SMT solver     mathematical constraint satisfaction
  ROPGadget         ARM gadget enumeration
  Manticore         symbolic execution engine
  pwntools          exploit development framework

Hardware Emulation
  QEMU              ARM instruction set emulation
  Renode            full spacecraft system emulation
  Raspberry Pi 4    real ARM hardware target
```

---

## 4. CCSDS Fuzzer Design

### 4.1 CCSDS TC Frame Structure

```
Telecommand Frame Structure (CCSDS 232.0-B-4):

 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─────────────────────────────────────────────────────────────────┤
│                    PRIMARY HEADER (48 bits)                     │
│  Version │ Bypass │ Control │ Reserved │ SCID │ VC ID │ Length  │
├─────────────────────────────────────────────────────────────────┤
│                  DATA FIELD HEADER (variable)                   │
│         Contains sequence counter and authentication data       │
├─────────────────────────────────────────────────────────────────┤
│                  APPLICATION DATA (variable)                    │
│              Telecommand payload — the actual command           │
├─────────────────────────────────────────────────────────────────┤
│                  FRAME ERROR CONTROL (16 bits)                  │
│                         CRC-16 checksum                         │
└─────────────────────────────────────────────────────────────────┘

Attack surfaces for fuzzing:
  Frame length field     — integer overflow potential
  VC ID field            — out of bounds array access
  Authentication MAC     — boundary condition in CryptoLib
  Sequence counter       — replay window logic bugs
  Application data size  — heap allocation size confusion
```

### 4.2 Grammar-Aware Mutation Strategy

```python
# Pseudocode — CCSDS grammar-aware mutator

class CCSDSMutator:
    def generate_seed_corpus(self):
        seeds = []

        # Valid frame — establishes baseline coverage
        seeds.append(self.build_valid_frame())

        # Length boundary conditions
        for length in [0, 1, 255, 256, 65535, 65536]:
            seeds.append(self.build_frame(length=length))

        # Authentication field boundaries
        for mac_len in [0, 8, 16, 32, 64]:
            seeds.append(self.build_frame(mac_length=mac_len))

        # Sequence counter edges
        for counter in [0, 0xFF, 0xFFFF, 0xFFFFFF]:
            seeds.append(self.build_frame(seq_counter=counter))

        # Version number confusion
        for version in [0, 1, 2, 3, 7]:
            seeds.append(self.build_frame(version=version))

        return seeds

    def mutate(self, seed):
        # AFL++ handles the actual mutation
        # This provides structured starting points
        pass
```

### 4.3 angr-Directed Seed Generation

```python
# Pseudocode — static analysis informed fuzzing

import angr

def generate_directed_seeds(binary_path):
    project = angr.Project(binary_path, auto_load_libs=False)

    # Find CryptoLib authentication function
    cfg = project.analyses.CFGFast()

    # Identify dangerous functions
    dangerous = []
    for func in cfg.functions.values():
        if any(call in func.name for call in
               ['memcpy', 'strcpy', 'malloc', 'crypto_tc']):
            dangerous.append(func)

    # Generate seeds that reach dangerous functions
    seeds = []
    for target in dangerous:
        # Symbolic execution to find input that reaches target
        state = project.factory.entry_state()
        simgr = project.factory.simulation_manager(state)
        simgr.explore(find=target.addr)

        if simgr.found:
            seed = simgr.found[0].posix.dumps(0)
            seeds.append(seed)

    return seeds
```

---

## 5. Zero-Day Discovery Pipeline

```
Phase 1: Corpus generation (Day 1-3)
  Generate CCSDS grammar-aware seed corpus
  Run angr static analysis on CryptoLib binary
  Generate seeds targeting authentication functions
  Estimated corpus size: 500-2000 seeds

Phase 2: Fuzzing (Day 3-14)
  AFL++ with LLVM instrumentation
  CmpLog enabled for magic byte solving
  Target: crypto_tc_process_security()
  M4 Max estimated throughput: 50,000 exec/sec
  Expected first crashes: Day 3-7

Phase 3: Crash triage (Ongoing)
  Automated crash deduplication
  AddressSanitizer for memory error classification
  Exploitability assessment via angr
  Controllable instruction pointer identification
  Stack vs heap corruption classification

Phase 4: Exploit development (Per crash)
  ROPGadget ARM gadget enumeration
  Z3 constraint solving for chain construction
  Manticore symbolic execution validation
  Working shellcode development
  pwntools for payload delivery

Expected finding classes:
  Heap buffer overflow in MAC verification
  Integer overflow in frame length parsing
  Use-after-free in session management
  Out-of-bounds read in sequence counter logic
```

---

## 6. ROP Chain Construction

### 6.1 ARM ROP Chain Pipeline

```
Step 1: Gadget discovery
  ROPGadget --binary libcryptolib.so --arch arm
  ROPGadget --binary cfs_core --arch thumb

  Gadget categories needed:
    Stack pivot     control SP register
    Register load   control R0-R7
    Memory write    write to arbitrary address
    Branch          jump to controlled address

Step 2: Constraint formulation (Z3)

  from z3 import *

  # Define gadgets as Z3 variables
  g1, g2, g3 = Ints('g1 g2 g3')

  # Constraints
  solver = Solver()

  # Must control PC (program counter)
  solver.add(gadgets[g1].sets_pc == True)

  # Must control R0 (first argument)
  solver.add(gadgets[g2].sets_r0 == True)

  # Chain must be stack aligned
  solver.add(chain_alignment(g1, g2, g3) == 0)

  # Solve
  if solver.check() == sat:
      model = solver.model()
      chain = build_chain(model)

Step 3: Manticore validation

  from manticore.native import Manticore

  m = Manticore(binary)

  @m.hook(target_address)
  def check_control(state):
      pc = state.cpu.PC
      if pc == shellcode_address:
          print("ROP chain achieves code execution")
          m.terminate()

  m.run()

Step 4: Proof output
  Mathematical proof: Z3 satisfiability certificate
  Empirical proof: Manticore execution trace
  Combined: "Code execution proven via constraint
             satisfaction AND symbolic execution"
```

---

## 7. Integration with The Fleet

```
CIPHER output feeds directly to The Fleet General:

{
  "cipher_finding": {
    "vulnerability_class": "heap_buffer_overflow",
    "cve_reference":       "CVE-2025-29912",
    "target_binary":       "libcryptolib.so",
    "target_function":     "crypto_tc_process_security",
    "exploit_type":        "rop_chain",
    "proof_method":        "z3_constraint_satisfaction",
    "proof_verified":      true,
    "shellcode_size":      248,
    "persistence":         "firmware_write",
    "sparta_mapping":      "EX-0009.03",
    "attck_mapping":       "T1203",
    "crew_safety_impact":  10,
    "chains_enabled": [
      "EX-0012.01 — Sensor spoofing via Modbus",
      "DE-0003    — Telemetry obfuscation",
      "EX-0001.01 — Command replay",
      "IMP-0002   — Station capture"
    ]
  }
}

The General receives this and reasons:
  "CIPHER has proven code execution on OBC.
   This is not a theoretical risk.
   This is a confirmed attack path.
   Breacher agent now has working payload.
   All downstream kill chain steps are enabled.
   Crew safety impact: CRITICAL.
   Priority: task Medic with CIPHER binary
   analysis data for immediate patch generation."
```

---

## 8. Demo Sequence

```
5-minute CIPHER demonstration:

0:00  Show cFS running in QEMU (ARM emulation)
      "This is NASA cFS — the same flight software
       framework Haven-1 runs. Running on ARM,
       same instruction set as the actual hardware."

1:00  Show AFL++ fuzzing CryptoLib
      Coverage graph growing in real time
      "We are fuzzing the CCSDS authentication
       handler. Watch the coverage map."

2:00  First crash appears
      "There it is. Heap buffer overflow in
       crypto_tc_process_security. The fuzzer
       found it in under 90 seconds on this run."

2:30  Show angr crash analysis
      "angr confirms this is an exploitable
       heap corruption. Instruction pointer
       is partially controllable."

3:00  Show Z3 solving the ROP chain
      "We feed the gadget list into Z3.
       It solves the constraint system and
       outputs the exact gadget sequence
       needed for code execution."

4:00  Show Manticore validation
      "Manticore symbolically executes the chain.
       Confirmed — the chain achieves arbitrary
       code execution on the OBC."

4:30  Show The Fleet General receiving the proof
      "The General receives CIPHER's output.
       It now has a working exploit, not a CVE
       reference. Every agent downstream gets
       real capability, not simulation."

5:00  Questions
```
