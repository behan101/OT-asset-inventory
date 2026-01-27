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
- [Step 7: Controlled Traffic Scenarios](#scenario-a--normal-operations-baseline)
    - [Scenario A - Normal Operations (Baseline)](#scenario-b--operator-activity-legitimate-write)
    - [Scenario B - Operator Activity (Legitimate Write)](#scenario-b--operator-activity-legitimate-write)
    - [Scenario C - Attack Simulation (Unauthorized Write)](#scenario-c--attack-simulation-unauthorized-write)
    - [Scenario D - Misconfigured or Rogue Behavior (Optional)](#scenario-d--misconfigured-or-rogue-behavior-optional)

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

Note: API changes may affect compatibility. Refer to the pymodbus API change log for updates (https://pymodbus.readthedocs.io/en/latest/source/api_changes.html).

---

# Step 1: Install Ubuntu 22.04 LTS on the OT VM

A headless (no-GUI) installation of **Ubuntu Server 22.04 LTS** was used for the OT VM. All tooling and scripts below assume this environment.

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

```python
from pymodbus.server import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusDeviceContext
)
import logging

# Enable Logging (SOC visibility)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Create device context
device = ModbusDeviceContext(
    di=ModbusSequentialDataBlock(0, [1]*10), # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0]*10), # Coils
    hr=ModbusSequentialDataBlock(0, [100]*10), # Holding Registers
    ir=ModbusSequentialDataBlock(0, [200]*10), # Input Registers
)

# Wrap in server context
context = ModbusServerContext(device, single=True)

# Start Modbus TCP Server
log.info("Starting Modbus TCP Server on port 502")

StartTcpServer(
    context=context,
    address=("0.0.0.0", 502)
)
```

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

```python
from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient("127.0.0.1", port=502)

if not client.connect():
    print("Failed to connect to Modbus server")
    exit(1)

print("Connected to Modbus server")

# Read holding registers
rr = client.read_holding_registers(0, count=5)
print("Holding Registers:", rr.registers)

# Write to a holding register (baseline)
client.write_register(1, 100)

# Write to a holding register (legitimate operator value)
# client.write_register(1, 120)

# Write to a holding register (simulated attack)
# client.write_register(1, 999)

time.sleep(1)

# Read again
rr = client.read_holding_registers(0, count=5)
print("Holding Registers after write:", rr.registers)

client.close
```

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

Create the polling client:

```bash
nano polling_client.py
```

```python
from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient("127.0.0.1", port=502)

if not client.connect():
    print("Failed to connect to Modbus server")
    exit(1)

print("SCADA connected to PLC")

while True:
    rr = client.read_holding_registers(0, count=5)
    if rr.isError():
        print("Read error")
    else:
        print("SCADA Poll:", rr.registers)

    time.sleep(3)
```

Run the SCADA client:

```bash
python polling_client.py
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
sudo ~/ot-venv/bin/python modbus_client.py
```
3. Let it run for 2–5 minutes
4. Do **not** run the HMI script.

**Expected behavior**:

* Repeated Modbus read requests
* No register value changes
* Predictable polling intervals

**Restoring Baseline State**:
If the HMI script was previously executed and register values were modified, the baseline state can be restored using one of the following methods:

Method 1 — Operator Reset (Preferred)
Modify the HMI script to write the original baseline value:
```py
client.write_register(1, 100)
```
This can be done by removing the comment hash on the desired line and adding comment hashes on the other scenarios. Run the script once to restore the register to its initial value.

Method 2 — PLC Restart
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
sudo ~/ot-venv/bin/python modbus_client.py
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
sudo ~/ot-venv/bin/python modbus_client.py
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
sudo ~/ot-venv/bin/python modbus_client.py
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

```python
from pymodbus.client import ModbusTcpClient
import time
import random

client = ModbusTcpClient("127.0.0.1", port=502)
client.connect()

while True:
    addr = random.randint(0, 5)
    value = random.randint(0, 2000)
    client.write_register(addr, value)
    print(f"Noisy write to register {addr}: {value}")
    time.sleep(10)
```

Run:

```bash
sudo ~/ot-venv/bin/python noisy_client.py
```

**What this simulates**:

* Compromised endpoint
* Malware-like behavior
* Unstable automation logic

---

