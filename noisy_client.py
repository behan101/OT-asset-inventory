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
