# OT Traffic Analysis — Modbus TCP

## Environment Overview

- Protocol: Modbus TCP
- Port: 502
- Assets:
  - PLC-01 (Modbus Server)
  - HMI-01 (Write Client)
  - SCADA-01 (Polling Client)

---

## Scenario A — Baseline

Observed Behavior:
- Repeated Modbus function code 03 (Read Holding Registers)
- Polling interval: ~3 seconds
- No write operations observed

Security Implications:
- Predictable polling pattern
- Cleartext protocol
- No authentication or integrity protection

---

## Scenario B — Legitimate Operator Write

Observed Behavior:
- One function code 06 (Write Single Register)
- Register 1 changed from 100 → 120
- Normal polling resumed

Security Implications:
- Write visible in cleartext
- No validation of authorized source
- No logging or alerting at PLC

---

## Scenario C — Unauthorized Write

Observed Behavior:
- One function code 06 (Write Single Register)
- Register 1 changed from 100 → 999
- Normal polling resumed

Security Implications:
- Malicious write indistinguishable from legitimate write
- No protocol security controls
- No detection or blocking
