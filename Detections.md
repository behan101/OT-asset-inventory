# OT Detection Engineering — Modbus

## Detection 1 — Any Modbus Write Command

Condition:
- Modbus function code 06 or 16 observed

Rationale:
- Writes should be rare and operator-authorized

Severity:
- High

---

## Detection 2 — Unsafe Register Values

Condition:
- Holding register 1 > 200

Rationale:
- Outside normal operating range

Severity:
- Critical

---

## Detection 3 — Write From Unauthorized Source

Condition:
- Modbus write not originating from HMI-01

Rationale:
- Indicates spoofing or compromise

Severity:
- Critical
