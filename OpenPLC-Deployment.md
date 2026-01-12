# OpenPLC on OT VM Deployment

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

Run the installer using the proper parameters for your OS (Linux in this case):
```
./install.sh linux
```
Now is when you may way to start the deployment of your IT/SOC/SecOps VM (See https://github.com/behan101/OT-asset-inventory/blob/main/IT-SOC-SecOps-Deployment.md)
