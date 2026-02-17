# Executive Summary — OT Asset Inventory & Traffic Analysis

## Project Background

Industrial control systems (ICS) and operational technology (OT) networks play a critical role in industrial processes. Unlike traditional IT systems, OT protocols (such as Modbus TCP) often lack built-in security features, making them difficult to monitor and protect with conventional security tools.

This project simulates a realistic OT environment using an OpenPLC server, HMI client, and SCADA polling logic. It generates Modbus TCP traffic and analyzes behavior under:

- Baseline conditions  
- Legitimate operator adjustments  
- Unauthorized or malicious register writes  

The goal is to evaluate OT traffic characteristics, identify detection opportunities, and frame SOC-relevant monitoring strategies.

---

## Key Findings

### 1. Modbus TCP Is Cleartext and Protocol-Limited

All traffic is unencrypted and unauthenticated:

- Function codes and register values are visible in transit  
- No mechanism exists in the protocol for access control, authentication, or integrity protection  
- SCADA polling (function code 03) is predictable and repetitive

These characteristics create inherent risk and visibility challenges.

### 2. Legitimate vs Unauthorized Writes Use the Same Protocol

Both operator and malicious writes use:

- Function code 06 (Write Single Register)  
- Same protocol structure  
- Differ only in value semantics

This means naive protocol detection cannot distinguish intent without context.

### 3. Baseline Behavior Is Key

The baseline (read-only polling) traffic serves as the SOC baseline. Any deviation — especially writes — should trigger inspection or alerting. Establishing this baseline is critical to subsequent detection engineering.

### 4. OT Scripts Should Always Be Planned and Controlled

The scenario scripts show how OT writes manifest on the wire and confirm how SCADA observes changes. While simulated, this mirrors real industrial control behavior.

---

## Traffic Scenarios and Business Impact

| Scenario | Behavior | Business Impact |
|----------|----------|-----------------|
| Baseline (A) | Read polling | Low — system stable |
| Legitimate Write (B) | Process value adjusted by operator | Medium — expected operation |
| Unauthorized Write (C) | Malicious value injected | High — potential process disruption |
| Noisy / Rogue (D) | Random writes | High — indicates malfunction or compromise |

Unauthorized writes pose **direct risk to physical processes**, potentially causing:

- Safety events  
- Operational outages  
- Equipment damage  
- Revenue loss  

Without detection, these events can go unnoticed until process impact occurs. For a more detailed traffic analysis, see [Traffic-Analysis.md](https://github.com/behan101/OT-asset-inventory/blob/main/Traffic-Analysis.md).

---

## Detection Opportunities

Using the captured traffic and analysis, the following detection opportunities emerge:

### Detection 1 — Unexpected Write Operations
Modbus Function Code 06 outside expected maintenance windows or from non-authorized hosts.

### Detection 2 — Out-of-Range Write Values
Write values beyond known good operational ranges (e.g., 999 in Scenario C).

### Detection 3 — Anomalous Write Frequency
Multiple writes in short intervals may indicate noise, scripting failures, or malware.

### Detection 4 — Unauthorized Source IP
Writes from systems other than known HMI/Engineering stations.

Detections can be implemented using:

- Suricata IDS signatures  
- Zeek scripts  
- SIEM analytics (correlating host + register changes)  

Detailed detection examples live in [Detections.md](https://github.com/behan101/OT-asset-inventory/blob/main/Detections.md).

---

## Recommendations

### Technical Controls

1. **Enforce segmentation between IT and OT**
   - Use firewalls and VLANs
   - Allow only expected Modbus flows

2. **Deploy passive OT monitoring**
   - Zeek / Suricata sensors on the OT perimeter
   - Monitor Modbus traffic flows

3. **Define baseline process behavior**
   - Document expected polling intervals
   - Identify expected write patterns

4. **Alert on anomalous command patterns**
   - Trigger alerts for function 06 outside operator maintenance windows
   - Correlate host identity with write actions

### Operational Controls

1. **Change management for PLC writes**
   - All writes must be authorized and logged

2. **Operator training**
   - Ensure operators understand ramifications of register writes

3. **Incident response readiness**
   - Playbooks for detection → validation → remediation

---

## Conclusion

Modbus TCP provides critical visibility into industrial process networks but lacks inherent security controls. By simulating and capturing real Modbus traffic, this project demonstrates how:

- Baseline traffic forms the foundation for detection
- Malicious writes are detectable only through context and anomaly logic
- SOC monitoring tools can be tuned for OT-specific threats

This project stands as a reusable OT SOC reference, bridging protocol behavior to SOC alerting strategies.

---

## Acknowledgements

This project used:

- OpenPLC v3
- Python pymodbus
- VirtualBox OT VM
- tcpdump packet capture
- Wireshark for analysis
