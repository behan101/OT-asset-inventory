# OpenPLC on OT VM Deployment

## Local VM (OT Zone) Creation
In this project, I used VirtualBox (https://www.virtualbox.org/) for the OT Subnet. Any virtual machine should perform similarly. If you have access to two or more virtual machines on the cloud, I would recommend you use those resources if you do not wish to run a local VM. At the time of creating this project, I only had access to one Azure virtual machine so I had to improvise using a local VM.

### Step 1: Install Ubuntu 22.04 LTS on the virtual machine.

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

Confirm that you are in the in the home directory then download and install Wireshark. You may want to install Wireshark requiring superuser privileges or root access in order to capture packets for security purposes.
```bash
sudo apt install python3 python3-pip wireshark -y
```

Be sure to create and use a virtual environment to isolate the project dependencies. Name your environment to something recognizable. In my case, I used `ot-venv`.
```bash
python3 -m venv ~/ot-venv
source ~/ot-venv/bin/activate
```

Download and install pymodbus:
```bash
pip3 install pymodbus modbus-tk
```

After installations, update all dependencies with `sudo apt upgrade && sudo apt install`. You may want to make sure the version of python and pip are compatable using the following commands:
```bash
python3 --version
pip3 --version
```

### Step 3: Simulate PLC (Modbus Server)

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

StartTcpServer(context=context, address=("0.0.0.0", 502))

```

Start the Modbus Server:
```bash
sudo python3 modbus_server.py
```
There should be validation and confirmation that the server is now running on port 502.

After confirmation that the server is running, open another terminal (ctrl+alt+2 on Linux Server) and logon to your ot-venv. You can navigate from terminal 1 and 2 by using alt+f1 (terminal 1) and alt+f2 (terminal 2). Once you are logged in, create a new file with the following command:
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
sudo ot-venv/bind/python modbus_client.py
```
The output should read:
```bash
Holding Registers: [100, 100, 100, 100, 100]
Holding Registers after write: [100, 999, 100, 100, 100]
```

If you have connectivity problems, check terminal 1 (modbus_server terminal) and make sure the server is on. You can terminate the server using ctrl+c while in the server terminal.

Note: This project uses pymodbus 3.12.x, python 3.12.3, and pip 24.0. There may be API changes and be subject to pymodbus API fragmentation. You may need to read documentation on API changes at https://pymodbus.readthedocs.io/en/latest/source/api_changes.html.

