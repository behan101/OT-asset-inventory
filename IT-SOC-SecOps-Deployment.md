# IT / SOC Deployment — OT Visibility & Monitoring Phase

## Index

- [Overview](#overview)
- [Objectives](#objectives)
- [High-Level Architecture](#high-level-architecture)
- [Monitoring Strategy](#monitoring-strategy)
- [SOC Tooling Options](#soc-tooling-options)
- [Chosen Approach for This Project](#chosen-approach-for-this-project)
- [Data Flow Design](#data-flow-design)
- [PCAP-Based Analysis vs Live Monitoring](#pcap-based-analysis-vs-live-monitoring)
- [Future Live OT-to-SOC Integration](#future-live-ot-to-soc-integration)
- [Project Boundaries and Assumptions](#project-boundaries-and-assumptions)
- [Next Steps (Future Implementations)](#next-steps)

---

# Overview

This phase of the project focuses on **IT/SOC-side visibility and monitoring** of OT network traffic generated from the simulated industrial environment.

The goal is to demonstrate how OT traffic—specifically Modbus TCP communications—can be:

- Ingested into SOC tooling  
- Analyzed for unsafe or unauthorized behavior  
- Used to develop detections and alerts  
- Investigated using standard SOC workflows  

This phase intentionally separates **OT operations** from **SOC monitoring**, reflecting real-world industrial network segmentation.

---

# Objectives

The primary objectives of the IT/SOC deployment phase are to:

- Analyze OT Modbus traffic from a defensive perspective  
- Understand how SOC tools interpret OT protocols  
- Develop detections for unsafe control actions  
- Simulate SOC investigation workflows  
- Maintain safe separation between IT and OT environments  

---

# High-Level Architecture

The project uses a **logical separation** between OT and IT environments.

```text
┌──────────────────────┐        ┌──────────────────────────┐
│ OT Virtual Machine   │        │ IT / SOC Environment     │
│                      │        │                          │
│ PLC / HMI / SCADA    │        │ SIEM / IDS / Analysis    │
│ Modbus TCP Traffic   │ -----> │ Zeek / Suricata / SIEM   │
│ tcpdump PCAPs        │        │ Wireshark / Detections   │
└──────────────────────┘        └──────────────────────────┘
```

At this stage, traffic is exported as PCAP files rather than streamed live.

This approach mirrors common SOC practices when:
- Investigating incidents after the fact
- Analyzing captures from OT tap devices
- Performing detection development offline

---

# Monitoring Strategy

Two monitoring strategies are considered in this project:

## 1. PCAP-Based Analysis (Current Phase)
- Traffic captured on the OT VM using tcpdump
- PCAPs transferred to the IT environment
- Analysis performed using Wireshark, Zeek, or IDS tools
- No live network connection between OT and IT

Advantages:
- Safe and controlled
- Easy to reproduce
- No risk to OT operations
- Ideal for learning and portfolio work

## 2. Live Network Monitoring (Future Phase)
- OT traffic mirrored or forwarded to SOC tools
- Requires careful network design and security controls
- More complex but closer to production environments

---

# SOC Tooling Options
The following SOC tools are commonly used to analyze OT traffic:
| Tool               | Purpose                            |
| ------------------ | ---------------------------------- |
| Wireshark          | Manual packet inspection           |
| Zeek               | Protocol-level transaction logging |
| Suricata           | IDS / IPS with Modbus rules        |
| Security Onion     | Full SOC platform                  |
| Elastic SIEM       | Centralized detection & alerting   |
| Microsoft Sentinel | Cloud-native SOC                   |

---

# Chosen Approach for This Project

For this project, the initial IT/SOC phase focuses on offline PCAP analysis.
This was chosen because:
- The OT VM and IT environment are intentionally isolated
- PCAPs are sufficient to demonstrate detection capability
- It reduces architectural complexity
- It aligns with SOC detection engineering workflows

Live monitoring can be added later as an enhancement.

---

# Data Flow Design
The data flow for this phase is as follows:
```text
OT VM
│
├── tcpdump (port 502)
│
├── scenario_a_baseline.pcap
├── scenario_b_legit_write.pcap
└── scenario_c_attack_write.pcap
│
▼
Shared Folder / Host System
│
▼
IT Analysis Environment
│
├── Wireshark Analysis
├── Zeek Parsing
└── Detection Development
```
No inbound traffic is ever sent from IT to OT.

---

# PCAP-Based Analysis vs Live Monitoring
| Aspect                | PCAP Analysis | Live Monitoring |
| --------------------- | ------------- | --------------- |
| Safety                | Very High     | Medium          |
| Complexity            | Low           | High            |
| Realism               | Medium        | High            |
| Detection Engineering | Excellent     | Excellent       |
| Risk to OT            | None          | Potential       |

For training, learning, and portfolio purposes, PCAP-based analysis is often preferred.

---

# Future Live OT-to-SOC Integration

A future enhancement may include:
- SPAN / port mirroring on the OT network
- Zeek or Suricata sensors listening passively
- One-way data diode or firewall-enforced flow
- Central SIEM ingestion

This would require:
- Additional network interfaces
- Firewall rules
- Strict access controls
- Change management

This project intentionally avoids those risks at this stage.

---

# Project Boundaries and Assumptions

To keep the project realistic and safe, the following assumptions apply:
- OT systems are not directly reachable from IT
- SOC has read-only visibility
- No authentication exists at the Modbus protocol level
- Detection relies on behavioral context, not protocol security

---

# Next Steps

With OT traffic now available to the SOC, the next phases of the project are:

## Phase 1 — Manual Analysis
- Inspect PCAPs in Wireshark
- Identify Modbus function codes
- Validate register writes

## Phase 2 — IDS & Detection Engineering
- Create Suricata Modbus rules
- Generate Zeek logs from PCAPs
- Identify anomalous write patterns

## Phase 3 — SOC Alerting
- Simulate alerts for:
- Unauthorized writes
- Abnormal register values
- Write frequency anomalies

## Phase 4 — Incident Response Narrative
- Build an OT security incident storyline
- Map attacker actions to MITRE ATT&CK for ICS
- Document analyst investigation steps

---
