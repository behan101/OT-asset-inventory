# OpenPLC on OT VM Deployment

## Local VM (OT Zone) Creation

### Step 1: Install Ubuntu 22.04 LTS on the virtual machine.

### Step 2: Install OT simulation tools

After deploying the Azure VM with Ubuntu Server installed (ubuntu-24_04-lts), updates were made to patch the system:
```
sudo apt update && sudo apt install
```
Then install python:
```
sudo apt install git python3 python3-pip -y
```

Next, clone the OpenPLC repository with the following command: 
```
git clone https://github.com/thiagoralves/OpenPLC_v3.git
```

Set the current directory to `OpenPLC_v3`:
```
cd OpenPLC_v3
```

Run the installer for OpenPLC using the proper parameters for your OS (Linux in this case):
```
./install.sh linux
```

Confirm that you are in the in the home directory then download and install Wireshark. You may want to install Wireshark requiring superuser privileges or root access in order to capture packets for security purposes.
```
sudo apt install python3 python3-pip wireshark -y
```

Download and install pymodbus:
```
pip3 install pymodbus modbus-tk
```

### Step 3: Simulate PLC (Modbus Server)
