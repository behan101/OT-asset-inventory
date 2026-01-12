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

Install using the proper parameters for your OS (Linux in this case):
```
./install.sh linux
```
