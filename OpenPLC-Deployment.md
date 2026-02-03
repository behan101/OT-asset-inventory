# OpenPLC on OT VM Deployment

# Index
- [Overview](#overview)
- [Architecture](#architecture)
- [Tooling Versions](#tooling-versions)
- [Step 1: Install Ubuntu 22.04 LTS on the OT VM](#step-1-install-ubuntu-2204-lts-on-the-ot-vm)
- [Step 2: Install OT Simulation Tools](#step-2-install-ot-simulation-tools)
- [Step 3: Create a Python Virtual Environment](#step-3-create-a-python-virtual-environment)
- [Step 4: Simulate a PLC Using a Modbus TCP Server](#step-4-simulate-a-plc-using-a-modbus-tcp-server)
- [Step 5: Simulate an HMI (Client)](#step-5-simulate-an-hmi-client)
- [Step 6: Simulate a SCADA System (Baseline Polling)](#step-6-simulate-a-scada-system-baseline-polling)
- [Logical OT Assets](#logical-ot-assets)
- [Step 7: Controlled Traffic Scenarios](#step-7-controlled-traffic-scenarios)
    - [Scenario A - Normal Operations (Baseline)](#scenario-a--normal-operations-baseline)
    - [Scenario B - Operator Activity (Legitimate Write)](#scenario-b--operator-activity-legitimate-write)
    - [Scenario C - Attack Simulation (Unauthorized Write)](#scenario-c--attack-simulation-unauthorized-write)
    - [Scenario D - Misconfigured or Rogue Behavior (Optional)](#scenario-d--misconfigured-or-rogue-behavior-optional)
- [Step 8: Install tcpdump on the OT VM](#step-8-install-tcpdump-on-the-ot-vm)

---

# Overview
This document describes how to deploy a small OT simulation environment using:
* A Modbus TCP–based PLC
* An HMI client
* A SCADA polling client

The environment is used to generate realistic OT network traffic for:
* Asset discovery
* Baseline behavior analysis
* Detection engineering
* SOC alert testing

---

# Architecture
In this project, I used VirtualBox (https://www.virtualbox.org/) to host the OT Zone. Any hypervisor or cloud VM would work similarly. Because my Azure subscription only allowed a single VM, I implemented a hybrid architecture:

Local VM → OT systems (PLC / HMI / SCADA)

Azure VM → IT-SOC and monitoring (added later)

This document covers only the **OT-side deployment and traffic simulation**.

---

# Tooling Versions

* Python: 3.12.x
* pip: 24.x
* pymodbus: 3.12.x

Note: API changes may affect compatibility. Refer to the pymodbus API change log for updates: (https://pymodbus.readthedocs.io/en/latest/source/api_changes.html).

---

# Step 1: Install Ubuntu 22.04 LTS on the OT VM

A headless (no-GUI) installation of **Ubuntu Server 22.04 LTS** was used for the OT VM. All tooling and scripts below assume this environment. When creating a user and password, I highly recommend a strong password since the server will be exposed to the internet. Be sure to write down or save your username and password.

---

# Step 2: Install OT Simulation Tools

Patch the system:

```bash
sudo apt update && sudo apt upgrade -y
```

Install Git and Python:

```bash
sudo apt install git python3 python3-pip python3-venv -y
```

Clone the OpenPLC repository:

```bash
git clone https://github.com/thiagoralves/OpenPLC_v3.git
cd OpenPLC_v3
```

Install OpenPLC:

```bash
./install.sh linux
```

---

# Step 3: Create a Python Virtual Environment

Create and activate a dedicated virtual environment to isolate OT dependencies:

```bash
python3 -m venv ~/ot-venv
source ~/ot-venv/bin/activate
```

Install Modbus libraries:

```bash
pip install pymodbus modbus-tk
```

Verify versions:

```bash
python3 --version
pip --version
```

---

# Step 4: Simulate a PLC Using a Modbus TCP Server

Create the server script:

```bash
nano modbus_server.py
```

Copy the script `modbus_server.py` (https://github.com/behan101/OT-asset-inventory/blob/main/modbus_server.py) and write out with `CTRL+O`


Start the PLC server (privileged port 502):

```bash
sudo ~/ot-venv/bin/python modbus_server.py
```

You should see:

```
INFO:root:Starting Modbus TCP Server on port 502
```

---

# Step 5: Simulate an HMI (Client)

Open a second terminal (`CTRL+ALT+F2`) and activate the venv:

```bash
source ~/ot-venv/bin/activate
```

Create the HMI client script:

```bash
nano modbus_client.py
```

Copy the script `modbus_client.py` (https://github.com/behan101/OT-asset-inventory/blob/main/modbus_client.py) and write out with `CTRL+O`.

Run the HMI script:

```bash
sudo ~/ot-venv/bin/python modbus_client.py
```

Expected output (Baseline):

```
Holding Registers: [100, 100, 100, 100, 100]
Holding Registers after write: [100, 100, 100, 100, 100]
```

---

# Step 6: Simulate a SCADA System (Baseline Polling)

Open a third terminal (`CTRL+ALT+F3`) and activate the venv:

```bash
source ~/ot-venv/bin/activate
```

Create the SCADA polling script:

```bash
nano polling_client.py
```

Copy the script `polling_client.py` (https://github.com/behan101/OT-asset-inventory/blob/main/polling_client.py) and write out with `CTRL+O`.

Run the SCADA client:

```bash
python polling_client.py
```

If the script does not run, try using the following command to ensure the virtual environment and proper privileges are running:

```bash
sudo ~/ot-venv/bin/python polling_client.py
```

You should see repeated output every three seconds:

```
SCADA Poll: [100, 100, 100, 100, 100]
```

---

# Logical OT Assets

Although all components run on one VM, they are treated as independent OT assets for inventory and risk analysis:

| Asset    | Script            | Behavior         |
| -------- | ----------------- | ---------------- |
| PLC-01   | modbus_server.py  | Serves registers |
| HMI-01   | modbus_client.py  | Reads and writes |
| SCADA-01 | polling_client.py | Constant polling |

---

# Step 7: Controlled Traffic Scenarios

## Scenario A — Normal Operations (Baseline)

1. Start the PLC server (`modbus_server.py`) in terminal 1:
```bash
sudo ~/ot-venv/bin/python modbus_server.py
```
2. Start the SCADA polling client (`polling_client.py`) in different terminal:
```bash
python polling_client.py
```
3. Let it run for 2–5 minutes
4. Do **not** run the HMI script.

**Expected behavior**:

* Repeated Modbus read requests
* No register value changes
* Predictable polling intervals

**Restoring Baseline State**:
If the HMI script was previously executed and register values were modified, the baseline state can be restored using one of the following methods:

**Method 1 — Operator Reset (Preferred)**
Modify the HMI script to write the original baseline value:
```py
client.write_register(1, 100)
```
This can be done by removing the comment hash on the desired line and adding comment hashes on the other scenarios. Run the script once to restore the register to its initial value.

**Method 2 — PLC Restart**
Stop and restart the Modbus server (modbus_server.py). This reinitializes all registers to their default values.

---

## Scenario B — Operator Activity (Legitimate Write)

### Step B1: Modify the HMI Script
Modify the HMI script to simulate a normal operator adjustment.

**Change only this line** in `modbus_client.py`:

```python
# legitimate operator write
client.write_register(1, 120)
```

Run the script once:

```bash
~/ot-venv/bin/python modbus_client.py
```

**What this simulates**:

* An authorized process change
* A safe control action
* Normal HMI behavior

**Expected SCADA output**:

```
SCADA Poll: [100, 120, 100, 100, 100]
```

### B2: Run Scenario B
Make sure the following are running:
* Terminal 1 (PLC)
```bash
sudo ~/ot-venv/bin/python modbus_server.py
```
* Terminal 3 (SCADA)
```bash
python polling_client.py
```
Then run the HMI Script once:
```bash
~/ot-venv/bin/python modbus_client.py
```
**Expected HMI output**:
```bash
Holding Registers: [100, 100, 100, 100, 100]
Holding Registers after write: [100, 120, 100, 100, 100]
```

**Expected SCADA output**:
```bash
SCADA Poll: [100, 120, 100, 100, 100]
```

---

## Scenario C — Attack Simulation (Unauthorized Write)

Revert the HMI script to the attack value:

```python
client.write_register(1, 999)
```
You can simply comment out the legitimate operator value and remove the hash `#` on the simulated attack register to run the script as a simulated attack.

Run the script once:

```bash
~/ot-venv/bin/python modbus_client.py
```

**What this simulates**:

* Malicious or unsafe register manipulation
* Unauthorized control action
* Process integrity violation

**Expected SCADA output**:

```
SCADA Poll: [100, 999, 100, 100, 100]
```

---

## Scenario D — Misconfigured or Rogue Behavior (Optional)

This simulates a compromised HMI, malware, or faulty automation logic.

Create `noisy_client.py`:
```bash
nano noisy_client.py
```

Copy the script `noisy_client.py` (https://github.com/behan101/OT-asset-inventory/blob/main/noisy_client.py) and write out with `CTRL+O`.

Run:

```bash
~/ot-venv/bin/python noisy_client.py
```

**What this simulates**:

* Compromised endpoint
* Malware-like behavior
* Unstable automation logic

---

# Step 8: Install tcpdump on the OT VM

Now that the scenarios are proven to be working properly, we can move on to packet capture. For this project, I used tcpdump since Wireshark does not work on a headless operating system without further complications. If you wish to use a GUI OS and install Wireshark, you may want to recreate the steps so far with a fresh install of Ubuntu Server with a GUI. To install tcpdump, use the following command in a terminal:
```bash
sudo apt install tcpdump -y
```

You are now ready to capture Modbus traffic for Scenarios A-D. Refer to https://github.com/behan101/OT-asset-inventory/blob/main/Traffic-Capture-Instructions.md

---
