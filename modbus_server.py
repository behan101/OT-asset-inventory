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
