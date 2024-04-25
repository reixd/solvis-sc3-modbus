from dataclasses import dataclass, is_dataclass, field
from enum import Enum, auto
from typing import Optional, Any, Iterator, List, Iterable

class SolvisZirkulationBetriebsartUnit(Enum):
    AUS = 0
    PULS = 1
    ZEIT = 2
    PULS_ZEIT = 3

class AnalogOutStatusUnit(Enum):
    AUTO_PWM = 0
    HAND_PWM = 1
    AUTO_ANALOG = 2
    HAND_ANALOG = 3

@dataclass
class Unit(object):

    def __str__(self) -> str:
        return self.scale
@dataclass
class TemperatureUnit(Unit):
    scale: str = "°C"
    unit: float = 0.1

    @staticmethod
    def validate(new_value: float) -> float:
        final_value = new_value * TemperatureUnit.unit  # Use class attribute or pass as argument
        if final_value >= 220.0:
            raise ValueError("Interruption Error")
        elif final_value <= -30.0:
            raise ValueError("Short Circuit Error")
        return final_value

@dataclass
class VolumeUnit(Unit):
    scale: str = "l/min"
    unit: float = 0.1

@dataclass
class SolvisModbusRegister:
    address: int
    description: str
    min: Optional[int]
    max: Optional[int]
    unit: Optional[Any] = None
    _value: Optional[Any] = field(default=None, repr=False, init=False)

    @property
    def value(self) -> Optional[Any]:
        return self._value

    @value.setter
    def value(self, new_value: Optional[Any]):
        # Check if 'unit' is a dataclass instance and has a 'validate' method
        if self.unit and hasattr(self.unit, 'validate'):
            new_value = self.unit.validate(new_value)  # Use the validate method

        # General range validation
        if self.min is not None and self.max is not None and new_value is not None:
            if not self.min <= new_value <= self.max:
                raise ValueError(f"Value '{new_value}' out of range (min={self.min}, max={self.max})")

        self._value = new_value

@dataclass
class SolvisModbusReadRegister(SolvisModbusRegister):
    pass

@dataclass
class SolvisModbusWriteRegister(SolvisModbusRegister):
    pass

class ReadInputRegistersEnum(SolvisModbusRegister, Enum):
    SETUP_1 = 0, "Setup 1", 0, 3, None
    SETUP_2 = 1, "Setup 2", 0, 3, None

    ZIRKULATION_MODE = 2049, "Zirkulation Betriebsart", 0, 3, SolvisZirkulationBetriebsartUnit

    ANALOG_OUT_1_STATUS = 3840, "Analog Out 1 Status", 0, 3, AnalogOutStatusUnit
    ANALOG_OUT_2_STATUS = 3845, "Analog Out 2 Status", 0, 3, AnalogOutStatusUnit
    ANALOG_OUT_3_STATUS = 3850, "Analog Out 3 Status", 0, 3, AnalogOutStatusUnit
    ANALOG_OUT_4_STATUS = 3855, "Analog Out 4 Status", 0, 3, AnalogOutStatusUnit
    ANALOG_OUT_5_STATUS = 3860, "Analog Out 5 Status", 0, 3, AnalogOutStatusUnit
    ANALOG_OUT_6_STATUS = 3865, "Analog Out 6 Status", 0, 3, AnalogOutStatusUnit

    UNIX_TIMESTAMP_HIGH = 32768, "Unix Timestamp high", None, None, None
    UNIX_TIMESTAMP_LOW = 32769, "Unix Timestamp low", None, None, None

    VERSION_SC3 = 32770, "Version SC3", None, None, None
    VERSION_NBG = 32771, "Version NBG", None, None, None

    TEMP_S1 = 33024, "Temp S1", None, None, TemperatureUnit()
    TEMP_S2 = 33025, "Temp S2", None, None, TemperatureUnit()
    TEMP_S3 = 33026, "Temp S3", None, None, TemperatureUnit()
    TEMP_S4 = 33027, "Temp S4", None, None, TemperatureUnit()
    TEMP_S5 = 33028, "Temp S5", None, None, TemperatureUnit()
    TEMP_S6 = 33029, "Temp S6", None, None, TemperatureUnit()
    TEMP_S7 = 33030, "Temp S7", None, None, TemperatureUnit()
    TEMP_S8 = 33031, "Temp S8", None, None, TemperatureUnit()
    TEMP_S9 = 33032, "Temp S9", None, None, TemperatureUnit()
    TEMP_S10 = 33033, "Temp S10", None, None, TemperatureUnit()
    TEMP_S11 = 33034, "Temp S11", None, None, TemperatureUnit()
    TEMP_S12 = 33035, "Temp S12", None, None, TemperatureUnit()
    TEMP_S13 = 33036, "Temp S13", None, None, TemperatureUnit()
    TEMP_S14 = 33037, "Temp S14", None, None, TemperatureUnit()
    TEMP_S15 = 33038, "Temp S15", None, None, TemperatureUnit()
    TEMP_S16 = 33039, "Temp S16", None, None, TemperatureUnit()

    VOLUME_FLOW_S17 = 33040, "Volumenstrom S17", None, None, VolumeUnit()
    VOLUME_FLOW_S18 = 33041, "Volumenstrom S17", None, None, VolumeUnit()

if __name__ == "__main__":
    # Example usage:

    print(80*'#')
    print(ReadInputRegistersEnum.ZIRKULATION_MODE)
    print(ReadInputRegistersEnum.ZIRKULATION_MODE.value)
    ReadInputRegistersEnum.ZIRKULATION_MODE.value = 3
    print(ReadInputRegistersEnum.ZIRKULATION_MODE.value)

    print(80*'#')
    print(ReadInputRegistersEnum.TEMP_S1)
    print(ReadInputRegistersEnum.TEMP_S1.value)
    print(ReadInputRegistersEnum.TEMP_S1.address)
    ReadInputRegistersEnum.TEMP_S1.value = 420
    print(ReadInputRegistersEnum.TEMP_S1.value)
    print(ReadInputRegistersEnum.TEMP_S1.unit)

    print(80*'#')
    print(ReadInputRegistersEnum.VOLUME_FLOW_S17)
    print(ReadInputRegistersEnum.VOLUME_FLOW_S17.value)
    print(ReadInputRegistersEnum.VOLUME_FLOW_S17.address)
    ReadInputRegistersEnum.VOLUME_FLOW_S17.value = 89
    print(ReadInputRegistersEnum.VOLUME_FLOW_S17.value)
    print(ReadInputRegistersEnum.VOLUME_FLOW_S17.unit)
