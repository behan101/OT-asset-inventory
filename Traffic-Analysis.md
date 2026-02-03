# Traffic Analysis — Modbus OT Simulation

## Index

- [Overview](#overview)
- [Captured Scenarios](#captured-scenarios)
- [Modbus Protocol Background](#modbus-protocol-background)
- [Scenario A: Baseline Polling](#scenario-a-baseline-polling)
- [Scenario B: Legitimate Operator Write](#scenario-b-legitimate-operator-write)
- [Scenario C: Unauthorized Write Attack](#scenario-c-unauthorized-write-attack)
- [Comparative Summary](#comparative-summary)
- [Detection Engineering Value](#detection-engineering-value)

---

# Overview

This document provides a structured analysis of Modbus TCP network traffic generated from the OT simulation environment in this project.

The objective is to demonstrate how Modbus traffic differs between:

- Normal SCADA baseline polling  
- Legitimate operator register writes  
- Unauthorized or malicious register manipulation  

These packet captures provide realistic OT protocol evidence that can be used for:

- OT asset discovery validation  
- Baseline behavior profiling  
- Detection engineering development  
- SOC alert testing and training  
- Industrial incident response practice  

---

# Captured Scenarios

Traffic was captured using `tcpdump` on port **502** (Modbus TCP).

The following scenario-based captures were generated:

| Scenario | File Name | Description |
|---------|----------|-------------|
| A | `scenario_a_baseline.pcap` | Normal SCADA polling (read-only traffic) |
| B | `scenario_b_legit_write.pcap` | Authorized operator write (value = 120) |
| C | `scenario_c_attack_write.pcap` | Unauthorized write attack (value = 999) |

---

# Modbus Protocol Background

Modbus TCP is a widely used industrial communication protocol found in OT environments.

It is commonly used between:

- PLCs (Programmable Logic Controllers)  
- HMIs (Human Machine Interfaces)  
- SCADA systems (Supervisory Control and Data Acquisition)  

Modbus traffic is composed of function codes, which define the requested operation.

The most relevant function codes in this project are:

| Function Code | Name | Meaning |
|-------------|------|---------|
| 03 | Read Holding Registers | Normal SCADA polling behavior |
| 06 | Write Single Register | Operator control action or malicious manipulation |

---

# Scenario A: Baseline Polling

## Description

Scenario A represents normal industrial monitoring behavior:

- SCADA continuously polls the PLC  
- No operator actions occur  
- Register values remain constant  

This traffic establishes a baseline for comparison.

## Expected Behavior

- Only Modbus reads (Function Code **03**)  
- Predictable polling interval  
- No register modifications  

## Wireshark Validation

Apply the following filter:

```wireshark
modbus.func_code == 3
```

## Observed:
- Repeated Read Holding Registers requests
- No write operations present

## Example SCADA Output:
```text
SCADA Poll: [100, 100, 100, 100, 100]
```

## Key Observation
Baseline traffic is stable, repetitive, and read-only.

---

# Scenario B: Legitimate Operator Write

## Description
Scenario B simulates a legitimate operator adjusting a process value.
The HMI performs a single authorized write:
```py
client.write_register(1, 120)
```

## Expected Behavior
- One Modbus write (Function Code 06)
- Register value changes from 100 → 120
- SCADA continues normal polling afterward

## Wireshark Validation
Filter for write operations:
```wireshark
modbus.func_code == 6
```

## Observed:
- A single Write Single Register request
- Register address: 1
- New value: 120

SCADA output confirms the change:
```text
SCADA Poll: [100, 120, 100, 100, 100]
```

## Key Observation
Operator writes are infrequent, intentional, and occur alongside normal polling.

---

# Scenario C: Unauthorized Write Attack

## Description
Scenario C simulates malicious or unauthorized manipulation of a PLC register.
The attacker writes an unsafe value:
```py
client.write_register(1, 999)
```

## Expected Behavior
- Function Code 06 write occurs
- Value is abnormal compared to baseline
- SCADA reflects unsafe process manipulation

## Wireshark Validation
Filter again:
```wireshark
modbus.func_code == 6
```

## Observed:
- A Write Single Register request
- Register address: 1
- New Value: 999

SCADA output:
```text
SCADA Poll: [100, 999, 100, 100, 100]
```

## Key Observation
Attack traffic can appear identical to operator traffic at the protocol level.
The difference is typically:
- Abnormal written values
- Unexpected source system
- Unusual timing or frequency
- Lack of authorization context

---

# Comparative Summary
| Scenario | Function Codes Seen | Register Change? | Security Meaning                    |
| -------- | ------------------- | ---------------- | ----------------------------------- |
| A        | 03 only             | No               | Normal baseline polling             |
| B        | 03 + one 06         | Yes (120)        | Legitimate operator control action  |
| C        | 03 + one 06         | Yes (999)        | Unauthorized or unsafe manipulation |

---

# Detection Engineering Value
This project highlights a core OT security challenge:
- Modbus has no authentication or built-in access control.
- Malicious writes look identical to legitimate writes.

Therefore, OT SOC detection must rely on contextual monitoring such as:
- Asset identity (who initiated the write?)
- Value thresholds (what was written?)
- Timing anomalies (when did it occur?)
- Write frequency (how often are writes happening?)
- Known-good engineering workstation behavior

Potential detection strategies include:
- Alert on any Function Code 06 in baseline environments
- Alert when register writes exceed safe operational ranges
- Alert when writes originate from unknown or unauthorized hosts
- Alert on repeated write bursts (possible malware or rogue logic)
