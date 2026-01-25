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
