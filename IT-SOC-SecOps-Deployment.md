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
- [Next Steps](#next-steps)

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
│ OT Virtual Machine   │        │ IT / SOC Environment      │
│                      │        │                          │
│ PLC / HMI / SCADA    │        │ SIEM / IDS / Analysis     │
│ Modbus TCP Traffic   │ -----> │ Zeek / Suricata / SIEM   │
│ tcpdump PCAPs        │        │ Wireshark / Detections   │
└──────────────────────┘        └──────────────────────────┘
