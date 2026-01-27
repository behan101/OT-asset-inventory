# Index
- [Step 1: Capture Traffic for Each Scenario](#step-1-capture-traffic-for-each-scenario)
- [Full State Reset + Re-Capture](#full-state-reset--re-capture)


# Step 1: Capture Traffic for Each Scenario

Run the baseline scenario and then capture traffic:
```bash
sudo tcpdump -i any port 502 -w scenario_a_baseline.pcap
```

Let SCADA (polling_client.py) run for 2-3 minutes in seperate terminal other than the modbus_server and then close the process with `CTRL+C`.

---

# Full State Reset + Re-Capture

If the scenario is misconfigured, use this method to reset the state and re-run the scenario for the another clean capture.

**Step 1**: Stop all processes
In all terminals, press `CTRL+C` to stop all processes.

Stop:
- PLC (modbus_server.py)
- SCADA (polling_client.py)
- Any HMI or noisy clients
- tcpdump (if running)

**Step 2**: Reset PLC state (Registers)
```bash
sudo ~/ot-venv/bin/python modbus_server.py
```
This restores:
- Holding Registers to `[100, 100, 100, 100, 100]`
- Coils, inputs, etc.

**Step 3**: Start SCADA Only (Baseline)
```bash
source ~/ot-venv/bin/activate
python polling_client.py
```

Confirm the output:
```bash
SCADA Poll: [100, 100, 100, 100, 100]
```

**Step 4**: Prepare the correct scenario in the HMI script
Open `modbus_client.py`
```bash
nano modbus_client.py
```

| Scenario | Write (Comment out the others) |
| -------- | ---------------- |
| A (Baseline) | `client.write_registers(1, 100)` |
| B (Legitimate Operator) | `client.write_registers(1, 120)` |
| C (Attack) | `client.write_registers(1, 999)` |

**Step 5**: Start the traffic capture
Use a scenario-specific filename:
```bash
sudo tcpdump -i any port 502 -w scenario_b_legit_write.pcap
```
or
```bash
sudo tcpdump -i any port 502 -w scenario_c_attack_write.pcap
```
Wait 5–10 seconds to capture baseline SCADA reads.

**Step 6**: Trigger the scenario
In another terminal:
```bash
sudo ~/ot-venv/bin/python modbus_client.py
```
Watch SCADA output change:
```bash
SCADA Poll: [100, 120, 100, 100, 100]
```
or
```bash
SCADA Poll: [100, 999, 100, 100, 100]
```

Remember to use the proper naming convention to help organize and avoid confusion:
```text
pcaps/
├── scenario_a_baseline.pcap
├── scenario_b_legit_write.pcap
├── scenario_c_attack_write.pcap
└── scenario_d_noisy_writes.pcap
```

---
