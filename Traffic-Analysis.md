# Traffic Analysis — Modbus OT Simulation

# Index

- [Overview](#overview)
- [Captured Scenarios](#captured-scenarios)
- [Modbus Protocol Background](#modbus-protocol-background)
- [Scenario A — Baseline Polling](#scenario-a--baseline-polling)
- [Scenario B — Legitimate Operator Write](#scenario-b--legitimate-operator-write)
- [Scenario C — Unauthorized Write Attack](#scenario-c--unauthorized-write-attack)
- [Comparative Summary](#comparative-summary)
- [Detection Engineering Value](#detection-engineering-value)
- [Next Steps](#next-steps)

---

# Overview

This document analyzes packet captures generated from the OT simulation environment in this project.

The goal is to demonstrate how Modbus TCP traffic differs between:

- Normal baseline polling
- Legitimate operator control actions
- Unauthorized or malicious register manipulation

These captures provide realistic OT network evidence that can be used for:

- SOC alert development
- Protocol-aware detection engineering
- OT asset discovery validation
- Incident response training

---

# Captured Scenarios

The following traffic captures were generated using `tcpdump`:

| Scenario | File Name | Description |
|---------|----------|-------------|
| A | `scenario_a_baseline.pcap` | SCADA polling only (read traffic) |
| B | `scenario_b_legit_write.pcap` | Authorized operator write (value = 120) |
| C | `scenario_c_attack_write.pcap` | Unauthorized write attack (value = 999) |

---

# Modbus Protocol Background

Modbus TCP is a common industrial protocol used for communication between:

- PLCs (controllers)
- HMIs (operator interfaces)
- SCADA systems (monitoring platforms)

Modbus operates using function codes.

The most relevant function codes in this project are:

| Function Code | Name | Meaning |
|-------------|------|---------|
| 03 | Read Holding Registers | Normal SCADA polling behavior |
| 06 | Write Single Register | Operator action or malicious modification |

---

# Scenario A — Baseline Polling

## Description

Scenario A represents normal OT monitoring behavior:

- SCADA continuously polls the PLC
- No HMI writes occur
- Register values remain constant

## Expected Behavior

- Only Modbus reads (Function Code 03)
- Predictable polling interval
- No process manipulation

## Wireshark Validation

Apply this filter:

```wireshark
modbus.func_code == 3
