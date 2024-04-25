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
class Temperature:
    value: float
    scale: str = "°C"
    unit: float = 0.1

    def __post_init__(self):
        self.final_value = self.value * self.unit
        if self.final_value >= 220.0:
            raise ValueError("Interruption Error")
        elif self.final_value <= -30.0:
            raise ValueError("Short Circuit Error")

@dataclass
class SolvisModbusRegister:
    address: int
    description: str
    min: Optional[int]
    max: Optional[int]
    unit: Optional[Any]

@dataclass
class SolvisModbusReadRegister(SolvisModbusRegister):
    pass

@dataclass
class SolvisModbusWriteRegister(SolvisModbusRegister):
    pass

class ReadInputRegistersEnum(Enum):
    SETUP_1 = SolvisModbusReadRegister(0, "Setup 1", 0, 3, None)
    SETUP_2 = SolvisModbusReadRegister(1, "Setup 2", 0, 3, None)

    ZIRKULATION_MODE = SolvisModbusReadRegister(2049, "Zirkulation Betriebsart", 0, 3, SolvisZirkulationBetriebsart)

    ANALOG_OUT_1_STATUS = SolvisModbusReadRegister(3840, "Analog Out 1 Status", 0, 3, AnalogOutStatus)
    ANALOG_OUT_2_STATUS = SolvisModbusReadRegister(3845, "Analog Out 2 Status", 0, 3, AnalogOutStatus)
    ANALOG_OUT_3_STATUS = SolvisModbusReadRegister(3850, "Analog Out 3 Status", 0, 3, AnalogOutStatus)
    ANALOG_OUT_4_STATUS = SolvisModbusReadRegister(3855, "Analog Out 4 Status", 0, 3, AnalogOutStatus)
    ANALOG_OUT_5_STATUS = SolvisModbusReadRegister(3860, "Analog Out 5 Status", 0, 3, AnalogOutStatus)
    ANALOG_OUT_6_STATUS = SolvisModbusReadRegister(3865, "Analog Out 6 Status", 0, 3, AnalogOutStatus)

    UNIX_TIMESTAMP_HIGH = SolvisModbusReadRegister(32768, "Unix Timestamp high", None, None, None)
    UNIX_TIMESTAMP_LOW = SolvisModbusReadRegister(32769, "Unix Timestamp low", None, None, None)

    VERSION_SC3 = SolvisModbusReadRegister(32770, "Version SC3", None, None, None)
    VERSION_NBG = SolvisModbusReadRegister(32771, "Version NBG", None, None, None)

    TEMP_S1 = SolvisModbusReadRegister(33024, "Temp S1*", None, None, Temperature)



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
