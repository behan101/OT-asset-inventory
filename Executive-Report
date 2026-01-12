# OT Asset Inventory: Modbus Traffic Analysis & Risk Assessment Report

## 1. Executive Summary

**Lab Title:** Hybrid OT Cybersecurity Lab (Azure + VirtualBox)

**Objective:**
Provide a concise summary of the lab scenario, goals, and outcomes. Describe what was tested, why it matters from an OT cybersecurity perspective, and the high-level results.

## **Key Takeaways:**

*
*

---

## 2. Lab Scope & Assumptions

**In Scope:**

* Simulated OT assets (PLC/HMI) hosted on local VirtualBox VM
* IT/Security monitoring hosted on Azure VM
* Modbus TCP communication
* Asset inventory, monitoring, and detection activities

**Out of Scope:**

* Production PLCs or live industrial systems
* Safety-instrumented systems (SIS)
* Proprietary vendor firmware

**Assumptions:**

* Lab represents a simplified manufacturing OT environment
* Availability and safety take precedence over confidentiality

---

## 3. Architecture Overview

**Environment Description:**
Describe the hybrid IT/OT architecture, including segmentation and connectivity.

**Zones & Conduits (IEC 62443):**

* IT Zone: Azure VM (Monitoring / SOC)
* OT Zone: VirtualBox VM (Simulated PLC/HMI)
* Conduit: VPN or SSH Port Forwarding

**Diagram:**
*(Insert architecture diagram here)*

---

## 4. Asset Inventory

| Asset Name | Zone | IP Address | Protocol | Function | Criticality |
| ---------- | ---- | ---------- | -------- | -------- | ----------- |
|            | OT   |            | Modbus   |          | High        |

**Notes:**

* Explain asset criticality and availability requirements

---

## 5. Threat Model & Risk Context

**Relevant Threats:**

* Unauthorized Modbus access
* Excessive polling impacting availability
* Lateral movement from IT to OT zone

**MITRE ATT&CK for ICS Techniques:**

* *(e.g., T0859 – Modify Controller Tasking)*

**Operational Risk Considerations:**

* Impact to availability and production
* Safety implications

---

## 6. Baseline Behavior Analysis

**Normal OT Traffic Characteristics:**

* Protocol: Modbus TCP
* Polling frequency:
* Approved source IPs:

**Evidence:**

* PCAP screenshots
* Wireshark filters used

---

## 7. Detection & Investigation

**Scenario Description:**
Describe the simulated anomalous or malicious activity.

**Detection Method:**

* Tool(s) used (Wireshark, SIEM, firewall logs)
* Indicators observed

**Timeline of Events:**

| Time | Event | Evidence |
| ---- | ----- | -------- |

---

## 8. Findings

## **Summary of Findings:**

*

**Severity Assessment:**

* Likelihood:
* Impact:
* Overall Risk Rating:

---

## 9. Remediation & Mitigation

**Recommended Actions:**

* Network segmentation changes
* Access control restrictions
* Monitoring improvements

**Availability Validation:**

* Describe how availability was confirmed after changes

---

## 10. Lessons Learned

## **What Worked Well:**

## **Challenges Encountered:**

## **Improvements for Future Iterations:**

---

## 11. Mapping to OT Security Standards

**IEC 62443:**

* Zones & Conduits
* Asset Identification
* Access Control

**NIST SP 800-82:**

* Asset Inventory
* Continuous Monitoring
* Incident Response

---

## 12. Conclusion

Summarize how this lab demonstrates OT cybersecurity concepts including asset visibility, detection, availability-aware remediation, and cross-zone risk management.

---

## 13. Appendix

**Tools Used:**

* Azure VM
* VirtualBox
* Wireshark
* pymodbus

**References:**

* IEC 62443
* NIST SP 800-82

---

## Disclaimer

This lab and report are for educational purposes only and do not represent a production OT environment.

---

**Author:** Brad Han
