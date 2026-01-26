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

# Write to a holding register (legitimate operator value)
client.write_register(1, 120)

# Write to a holding register (simulated attack)
#client.write_register(1, 999)

time.sleep(1)

# Read again
rr = client.read_holding_registers(0, count=5)
print("Holding Registers after write:", rr.registers)

client.close()
