from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Any, Iterator, List, Iterable

class SolvisZirkulationBetriebsart(Enum):
    AUS = 0
    PULS = 1
    ZEIT = 2
    PULS_ZEIT = 3

class AnalogOutStatus(Enum):
    AUTO_PWM = 0
    HAND_PWM = 1
    AUTO_ANALOG = 2
    HAND_ANALOG = 3

@dataclass
class SolvisModbusRegister:
    address: int
    description: str
    min: int
    max: int
    unit: Optional[Any]

@dataclass
class SolvisModbusReadRegister(SolvisModbusRegister):
    pass
class SolvisModbusWriteRegister(SolvisModbusRegister):
    pass

class ReadInputRegistersEnum(Enum):
    SETUP_1 = SolvisModbusReadRegister(0, "Setup 1", 0, 3, None)
    SETUP_2 = SolvisModbusReadRegister(1, "Setup 2", 0, 3, None)
    ZIRKULATION_MODE = SolvisModbusReadRegister(2049, "Zirkulation Betriebsart", 0, 3, SolvisZirkulationBetriebsart)
    OUTPUT_STATUS = SolvisModbusReadRegister(3840, "Analog Out 1 Status", 0, 3, AnalogOutStatus)

class SolvisSC3ModbusRegisters:
    def __init__(self, registers: Iterable):
        # Initialize registers from the enum
        self.registers = {reg.value.address: reg.value for reg in registers}

    def __getitem__(self, address: int) -> SolvisModbusRegister:
        return self.registers[address]

    def __setitem__(self, address: int, value: SolvisModbusRegister):
        self.registers[address] = value

    def __delitem__(self, address: int):
        del self.registers[address]

    def __iter__(self) -> Iterator[int]:
        return iter(self.registers)

    def __len__(self):
        return len(self.registers)

    def __repr__(self):
        return f"{self.registers}"

if __name__ == "__main__":
    # Example usage:
    modbus_table = SolvisSC3ModbusRegisters(ReadInputRegistersEnum)
    print(modbus_table)
    print(modbus_table[2049])  # Access like a dictionary
    print(modbus_table[2049].description)
    print(modbus_table[2049].address)
