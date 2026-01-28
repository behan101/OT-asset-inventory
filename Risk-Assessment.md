
# OT Risk Assessment — Modbus Environment

## Identified Risks

| Risk ID | Description | Impact | Likelihood | Priority |
|--------|-------------|--------|------------|----------|
| R-01 | Unauthorized Modbus writes | Process disruption | High | Critical |
| R-02 | Cleartext protocol | Command interception | Medium | High |
| R-03 | No protocol authentication | Spoofed control | High | Critical |
| R-04 | Flat OT host | Lateral movement | Medium | High |
| R-05 | No monitoring | Delayed detection | Medium | High |

---

## Methodology

- Availability prioritized over confidentiality  
- Process integrity prioritized over data protection  
- No active scanning performed against PLC  
- Downtime considered severe impact  

Aligned with:
- NIST SP 800-82  
- IEC 62443
