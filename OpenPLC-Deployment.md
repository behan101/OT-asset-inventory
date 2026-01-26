# OpenPLC on OT VM Deployment

## Local VM (OT Zone) Creation
In this project, I used VirtualBox (https://www.virtualbox.org/) for the OT Subnet. Any virtual machine should perform similarly. If you have access to two or more virtual machines on the cloud, I would recommend you use those resources if you do not wish to run a local VM. At the time of creating this project, I only had access to one Azure virtual machine so I had to improvise using a local VM.

### Step 1: Install Ubuntu 22.04 LTS on the virtual machine.

I installed a headless (No GUI) installation of Ubuntu Server due to preference. This project will be based on this installation and may differ from GUI installation versions.

### Step 2: Install OT simulation tools

After deploying the Azure VM with Ubuntu Server installed (ubuntu-24_04-lts), updates were made to patch the system:
```bash
sudo apt update && sudo apt install
```
Then install python:
```bash
sudo apt install git python3 python3-pip -y
```

Next, clone the OpenPLC repository with the following command: 
```bash
git clone https://github.com/thiagoralves/OpenPLC_v3.git
```

Set the current directory to `OpenPLC_v3`:
```bash
cd OpenPLC_v3
```

Run the installer for OpenPLC using the proper parameters for your OS (Linux in this case):
```bash
./install.sh linux
```

Be sure to create and use a virtual environment to isolate the project dependencies. Name your environment to something recognizable. In my case, I used `ot-venv`.
```bash
python3 -m venv ~/ot-venv
source /ot-venv/bin/activate
```

While in the new `ot-venv`, download and install pymodbus:
```bash
pip3 install pymodbus modbus-tk
```

After installations, update all dependencies with `sudo apt upgrade && sudo apt install`. You may want to make sure the version of python and pip are compatable using the following commands:
```bash
python3 --version
pip3 --version
```

### Step 3: Simulate PLC (Programmable Logic Controller) / HMI (Human-Machine Interface) / SCADA (Supervisory Control and Data Acquisition) with Modbus Server

Create a simple Modbus Server by using the Linux CLI to open the `modbus_server.py` file using nano:
```bash
nano modbus_server.py
```

Then copy, paste, and write out the the Modbus Server Script for OT VM:
```py
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

Start the Modbus Server:
```bash
sudo ot-venv/bin/python modbus_server.py
```
There should be validation and confirmation that the server is now running on port 502.

After confirmation that the server is running, open another terminal using `CTRL+ALT+F2` on Linux Ubuntu Server, and logon to your ot-venv. You can navigate from terminal 1 and 2 by using `ALT+F1` (terminal 1) and `ALT+F2` (terminal 2). Once you are logged in, create a new file with the following command:
```bash
nano modbus_client.py
```

This should open up a script for the `modbus_client.py` file. Add the following to the file and write out to save the changes:
```py
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

# Write to a holding register (simulated attack)
client.write_register(1, 999)

time.sleep(1)

# Read again
rr = client.read_holding_registers(0, count=5)
print("Holding Registers after write:", rr.registers)

client.close()
```
In terminal 2 (modbus_client terminal), run the client with:
```bash
sudo ot-venv/bin/python modbus_client.py
```
The output should read:
```bash
Holding Registers: [100, 100, 100, 100, 100]
Holding Registers after write: [100, 999, 100, 100, 100]
```

If you have connectivity problems, check terminal 1 (modbus_server terminal) and make sure the server is on. You can terminate the server using `ctrl+c` while in the server terminal.

Note: This project uses pymodbus 3.12.x, python 3.12.3, and pip 24.0. There may be API changes and be subject to pymodbus API fragmentation. You may need to read documentation on API changes at https://pymodbus.readthedocs.io/en/latest/source/api_changes.html.

Now that the server and client are running properly, we need to simulate traffic using a script. Open a third terminal using `CTRL+ALT+F3`, then create a file called `polling_client.py` using the following command:
```bash
nano polling_client.py
```
Write out the following script in the new polling_client.py file:
```py
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

Now start the OT-ENV and run the polling_client:
```bash
source ~/ot-venv/bin/activate
python polling_client.py
```
If setup correctly, the command line should return the following with an interval of three seconds:
```bash
SCADA Poll: [100, 999, 100, 100, 100]
```

We now have three logical OT Assets and have a fully simulated OT environment.
| Asset    | Script            | Behavior         |
| -------- | ----------------- | ---------------- |
| PLC-01   | modbus_server.py  | Serves registers |
| HMI-01   | modbus_client.py  | Reads + writes   |
| SCADA-01 | polling_client.py | Constant polling |

### Step 4: Create Controlled Traffic Scenarios

#### Scenario A: Normal Operations (Baseline)
1. Start the PLC server (modbus_server.py)
2. Start SCADA polling client (polling_client.py)
3. Let it run for 2-5 minutes
4. Do not run the HMI write script (modbus_client.py)

This scenario should result in clean Modbus reads with predictable polling and no register changes.

#### Scenario B: Operator Activity (Legitimate Write)
Modify the HMI script slightly (modbus_client.py):
```py
# legitimate operator write
client.write_register(1, 120)
```
Run this script one time. This will simulate a normal process adjustment and an authorized register write.

#### Scenario C: Attack Simulation (Unauthorized Write)
The existing logic:
```py
client.write_register(1, 999)
```
This simulates malicious or an unsafe write and process manipulation.

#### Scenario D: Misconfigured or Rogue Behavior
The following script simulates a compromised HMI, malware, or faulty automation script:
```py
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
