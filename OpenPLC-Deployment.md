# OpenPLC on OT VM Deployment

## Local VM (OT Zone) Creation

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
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*50),
    co=ModbusSequentialDataBlock(0, [0]*50),
    hr=ModbusSequentialDataBlock(0, [120]*50),
    ir=ModbusSequentialDataBlock(0, [0]*50)
)

context = ModbusServerContext(slaves=store, single=True)

print("OT Modbus PLC simulation running on TCP/502")
StartTcpServer(context, address=("0.0.0.0", 502))
```

Start the Modbus Server:
```bash
sudo python3 modbus_server.py
```
