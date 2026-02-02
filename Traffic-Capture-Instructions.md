# Index
- [Capture Traffic for Each Scenario](#capture-traffic-for-each-scenario)
- [Scenario A: Baseline](#scenario-a-baseline)
- [Scenario B: Operator Activity (Legitimate Write)](#scenario-b-operator-activity-legitimate-write)
- [Scenario C: Attack Simulation (Unauthorized Write)](#scenario-c-attack-simulation-unauthorized-write)
- [Full State Reset + Re-Capture](#full-state-reset--re-capture)
- [Captured Traffic Scenarios](#captured-traffic-scenarios)
- [Viewing PCAP Files](#viewing-pcap-files)
- [Local VM (OT VM) Shared Folder to Host](#local-vm-ot-vm-shared-folder-to-host)

# Capture Traffic for Each Scenario

## Scenario A: Baseline

Run the baseline scenario (https://github.com/behan101/OT-asset-inventory/blob/main/OpenPLC-Deployment.md#scenario-a--normal-operations-baseline).
```bash
sudo tcpdump -i any port 502 -w scenario_a_baseline.pcap
```
Let SCADA run for 30 seconds before starting tcpdump. Capture traffic for about 30–60 seconds total, then stop with `CTRL+C`.

---

## Scenario B: Operator Activity (Legitimate Write)

After running scenario A, start the packet capture for Scenario B:
```bash
sudo tcpdump -i any port 502 -w scenario_b_legitwrite.pcap
```
Once the capture has started, edit the modbus_client.py (HMI) script and configure it for scenario B. Then run the script.

After 30 seconds of capturing traffic, including the write, close the operation with `CTRL+C` in the tcpdump terminal.

---

## Scenario C: Attack Simulation (Unauthorized Write)

After running scenario B, start the packet capture for Scenario C:
```bash
sudo tcpdump -i any port 502 -w scenario_c_attack_write.pcap
```
Once the capture has started, edit the modbus_client.py (HMI) script and configure it for scenario C. Then run the script.

After 30 seconds of capturing traffic, including the write, close the operation with `CTRL+C` in the tcpdump terminal.

---

# Full State Reset + Re-Capture

If the scenario is misconfigured, use this method to reset the state and re-run the scenario for the another clean capture.

## Step 1: Stop all processes
In all terminals, press `CTRL+C` to stop all processes.

Stop:
- PLC (modbus_server.py)
- SCADA (polling_client.py)
- Any HMI or noisy clients
- tcpdump (if running)

## Step 2: Reset PLC state (Registers)
```bash
sudo ~/ot-venv/bin/python modbus_server.py
```
This restores:
- Holding Registers to `[100, 100, 100, 100, 100]`
- Coils, inputs, etc.

## Step 3: Start SCADA Only (Baseline)
```bash
source ~/ot-venv/bin/activate
python polling_client.py
```

Confirm the output:
```bash
SCADA Poll: [100, 100, 100, 100, 100]
```

## Step 4: Prepare the correct scenario in the HMI script
Open `modbus_client.py`
```bash
nano modbus_client.py
```

| Scenario | Write (Comment out the others) |
| -------- | ---------------- |
| A (Baseline) | `client.write_register(1, 100)` |
| B (Legitimate Operator) | `client.write_register(1, 120)` |
| C (Attack) | `client.write_register(1, 999)` |

## Step 5: Start the traffic capture
Use a scenario-specific filename:
```bash
sudo tcpdump -i any port 502 -w scenario_b_legitwrite.pcap
```
or
```bash
sudo tcpdump -i any port 502 -w scenario_c_attack_write.pcap
```
Wait 5–10 seconds to capture baseline SCADA reads.

## Step 6: Trigger the scenario
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
├── scenario_b_legitwrite.pcap
├── scenario_c_attack_write.pcap
└── scenario_d_noisy_writes.pcap
```

---

# Captured Traffic Scenarios

The following packet captures were generated from the OT simulation environment.

## Scenario A — Baseline Operations
Description:
- SCADA polling only
- No HMI writes
- Stable register values

Expected Behavior:
- Modbus function code 03 only
- Predictable polling interval

---

## Scenario B — Legitimate Operator Write
Description:
- HMI writes value 120 to holding register 1
- Normal polling resumes

Expected Behavior:
- One Modbus function code 06
- Followed by function code 03 polling

---

## Scenario C — Unauthorized Write (Attack Simulation)
Description:
- HMI writes value 999 to holding register 1
- Unsafe process value introduced

Expected Behavior:
- One Modbus function code 06
- Followed by function code 03 polling

---

# Viewing PCAP Files

GitHub cannot preview `.pcap` files directly.

To inspect the captured traffic:

1. Download the file from the `pcaps/` directory
2. Open it locally using Wireshark:

---

# Local VM (OT VM) Shared Folder to Host

## Step 1: Create / Mount Shared Folder
In order to open the packet captures from the local VM, I recommend using a shared folder from the host machine to the local VM. If using VirtualBox, create a folder somewhere on your host machine such as `C:\OT-PCAPS`.
Then open Virtualbox and select your Ubuntu Server OT VM:
- Click settings
- Go to Shared Folders
- Add a folder

Configure the Shared Folder by giving the proper Folder Path on your host machine (C:\OT-PCAPs for example). Under Folder Name, write `OT-PCAPS`. Check Auto-mount and Make Permanent.

---

## Step 2: Install VirtualBox Guest Additions

While logged on in the OT VM Ubuntu Server, run an update and install VirtualBox Guest Utilities.
```bash
sudo apt update
sudo apt install virtualbox-guest-utils -y
```
Then reboot the server:
```bash
sudo reboot
```

---

## Step 3: Verify the Shared Folder is Mounted

After the reboot, login to the terminal and check to see if the folder is mounted properly:
```bash
sudo ls /media
```
You should see a folder named `sf_OT-PCAPS`.

---

## Step 4: Copy PCAP files into the Shared Folder

Copy the scenario PCAPS:
```bash
sudo cp scenario_a_baseline.pcap /media/sf_OT-PCAPS/
sudo cp scenario_b_legitwrite.pcap /media/sf_OT-PCAPS/
sudo cp scenario_c_attack_write.pcap /media/sf_OT-PCAPS/
```
The PCAP files should now be accessible in the shared folder of the host computer. You can use these to upload them to Github or inspect them using Wireshark.
