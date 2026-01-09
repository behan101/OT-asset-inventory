
### Segmentation Rationale
- IT and OT systems are isolated using Azure Network Security Groups (NSGs)
- Only required industrial traffic (Modbus TCP, port 502) is permitted between zones
- This design aligns with IEC 62443 zone and conduit principles

---

## Tools & Technologies

### Cloud & Infrastructure
- Microsoft Azure
- Azure Virtual Network & Network Security Groups
- Linux Virtual Machines (Ubuntu)

### OT Simulation
- OpenPLC Runtime
- Modbus TCP protocol
- Python Modbus client (pymodbus)

### Security & Analysis
- Wireshark / tcpdump
- Nmap (safe, limited usage)
- Python (traffic generation & analysis)

---

## Simulated OT Assets

| Asset Name | Type | Location | Protocol | Criticality |
|----------|------|---------|---------|------------|
| PLC-01 | PLC | OT VM | Modbus TCP | High |
| HMI-01 | HMI | OT VM | Modbus TCP | High |
| SCADA-01 | SCADA | OT VM | Modbus TCP | High |

> Note: Although multiple OT roles run on a single VM for lab purposes, assets are treated as independent logical OT systems for inventory and risk analysis.

---

## Lab Objectives

- Build and maintain an OT asset inventory
- Observe and analyze industrial network traffic
- Identify OT-specific security risks
- Prioritize vulnerabilities based on availability and operational impact
- Recommend OT-safe security controls

---

## Industrial Traffic Analysis

Modbus TCP traffic was generated between simulated OT components and captured from the IT monitoring VM. Packet analysis revealed:

- Cleartext communications
- Read and write function codes visible in transit
- No authentication or encryption
- Predictable polling behavior

These characteristics reflect real-world OT protocol limitations and emphasize the importance of segmentation and monitoring.

---

## Identified Risks

| Risk | Impact | Likelihood | Priority |
|----|-------|-----------|---------|
| Unauthorized Modbus write commands | Process disruption / outage | Medium | High |
| Flat OT host architecture | Lateral movement | Medium | High |
| Lack of OT monitoring | Delayed detection | Medium | High |
| No authentication on protocol | Unauthorized control | High | Critical |

---

## Risk Prioritization Approach

Risk was evaluated using OT-focused criteria:
- Availability and safety prioritized over confidentiality
- Operational downtime considered more impactful than data exposure
- No active vulnerability scanning performed against PLC processes

This approach aligns with NIST SP 800-82 and IEC 62443 guidance.

---

## Recommended Mitigations

- Enforce strict IT/OT segmentation using firewall rules
- Limit Modbus access to authorized sources only
- Deploy passive OT network monitoring
- Implement change management and access control procedures
- Avoid active scanning on OT systems during production operations

---

## Standards & Frameworks Referenced

- IEC 62443 (Zones & Conduits)
- NIST SP 800-82 (ICS Security)
- MITRE ATT&CK for ICS (Conceptual Mapping)

---

## Key Takeaways

- OT security requires asset-centric and availability-aware thinking
- Many industrial protocols lack native security controls
- Network segmentation and visibility are foundational OT security controls
- Cloud platforms can be used safely for OT security simulation and learning

---

## Future Enhancements

- Add passive IDS (Suricata) for Modbus alerting
- Create detection logic for unauthorized write commands
- Expand asset inventory with firmware tracking
- Add centralized logging and dashboards

---

## Disclaimer

This lab is for educational purposes only. No production OT systems were accessed, scanned, or impacted.

---

## Author
Brad Han  
GitHub: https://github.com/behan101  
LinkedIn: https://www.linkedin.com/in/brad-han/
