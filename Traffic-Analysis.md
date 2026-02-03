# Traffic Analysis — Modbus OT Simulation

## Index

- [Overview](#overview)
- [Captured Scenarios](#captured-scenarios)
- [Modbus Protocol Background](#modbus-protocol-background)
- [Scenario A — Baseline Polling](#scenario-a--baseline-polling)
- [Scenario B — Legitimate Operator Write](#scenario-b--legitimate-operator-write)
- [Scenario C — Unauthorized Write Attack](#scenario-c--unauthorized-write-attack)
- [Comparative Summary](#comparative-summary)
- [Detection Engineering Value](#detection-engineering-value)
- [Recommended Wireshark Evidence](#recommended-wireshark-evidence)
- [Next Steps](#next-steps)

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

# Scenario A — Baseline Polling

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
