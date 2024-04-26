from dataclasses import dataclass, is_dataclass, field
from enum import Enum, auto
from typing import Optional, Any, Iterator, List, Iterable

class SolvisZirkulationBetriebsartEnum(Enum):
    AUS = 0
    PULS = 1
    ZEIT = 2
    PULS_ZEIT = 3

class AnalogOutStatusEnum(Enum):
    AUTO_PWM = 0
    HAND_PWM = 1
    AUTO_ANALOG = 2
    HAND_ANALOG = 3


class HeatingCircuitStatesEnum(Enum):
    AUTOMATIC = 2           # Automatik
    DAY_MODE = 3            # Tagbetrieb
    REDUCED_OPERATION = 4   # Absenkbetrieb
    STANDBY = 5             # Standby
    ECO = 6                 # Eco
    HOLIDAY = 7             # Urlaub

class ErrorIndicatorEnum(Enum):
    FUSE_POWER_SUPPLY_MODULE = 0
    BURNER_ERROR = 1
    STB1_ERROR = 2
    STB2_ERROR = 3
    BURNER_CM424 = 4
    SOLAR_PRESSURE = 5
    NOT_DEFINED = 6     # The name of this value is empty in the specification v1.0 as of 09.2021
    SYSTEM_PRESSURE = 7
    CONDENSATE = 8

@dataclass
class Unit(object):
    unit: str

    def __str__(self) -> str:
        return self.unit
@dataclass
class TemperatureUnit(Unit):
    unit: str = "°C"
    scale: float = 0.1

    @staticmethod
    def validate(new_value: float) -> float:
        final_value = new_value * TemperatureUnit.scale  # Use class attribute or pass as argument
        if final_value >= 220.0:
            raise ValueError("Interruption Error")
        elif final_value <= -30.0:
            raise ValueError("Short Circuit Error")
        return final_value

@dataclass
class VolumeUnit(Unit):
    unit: str = "l/min"
    scale: float = 0.1

    @staticmethod
    def validate(new_value: float) -> float:
        final_value = new_value * VolumeUnit.scale  # Use class attribute or pass as argument
        return final_value

@dataclass
class AmpereUnit(Unit):
    unit: str = "mA"

@dataclass
class VoltUnit(Unit):
    unit: str = "V"
    scale: float = 0.1

    @staticmethod
    def validate(new_value: float) -> float:
        final_value = new_value * VoltUnit.scale  # Use class attribute or pass as argument
        return final_value

@dataclass
class PercentageUnit(Unit):
    unit: str = "%"
    scale: float = 100

    def __init__(self, scale: float = 100):
        self.scale = scale

    @staticmethod
    def validate(new_value: float) -> float:
        final_value = new_value / PercentageUnit.scale  # Use class attribute or pass as argument
        return final_value

@dataclass
class PWMUnit(PercentageUnit):
    unit: str = "% (PWM)"

@dataclass
class WattUnit(Unit):
    unit: str = "W"

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

    ZIRKULATION_MODE = 2049, "Zirkulation Betriebsart", 0, 3, SolvisZirkulationBetriebsartEnum

    ANALOG_OUT_1_STATUS = 3840, "Analog Out 1 Status", 0, 3, AnalogOutStatusEnum
    ANALOG_OUT_2_STATUS = 3845, "Analog Out 2 Status", 0, 3, AnalogOutStatusEnum
    ANALOG_OUT_3_STATUS = 3850, "Analog Out 3 Status", 0, 3, AnalogOutStatusEnum
    ANALOG_OUT_4_STATUS = 3855, "Analog Out 4 Status", 0, 3, AnalogOutStatusEnum
    ANALOG_OUT_5_STATUS = 3860, "Analog Out 5 Status", 0, 3, AnalogOutStatusEnum
    ANALOG_OUT_6_STATUS = 3865, "Analog Out 6 Status", 0, 3, AnalogOutStatusEnum

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

    ANALOG_IN_1 = 33042, "Analog In 1", None, None, VoltUnit()
    ANALOG_IN_2 = 33043, "Analog In 2", None, None, VoltUnit()
    ANALOG_IN_3 = 33044, "Analog In 3", None, None, VoltUnit()

    DIGITAL_INPUT_ERRORS = 33045, "DigIn Störungen", None, None, ErrorIndicatorEnum

    OUTPUT_A1 = 33280, "Ausgang A1", 0, 100, PercentageUnit()
    OUTPUT_A2 = 33280, "Ausgang A2", 0, 200, PercentageUnit(200)
    OUTPUT_A3 = 33280, "Ausgang A3", 0, 100, PercentageUnit()
    OUTPUT_A4 = 33280, "Ausgang A4", 0, 100, PercentageUnit()
    OUTPUT_A5 = 33280, "Ausgang A5", 0, 100, PercentageUnit()
    OUTPUT_A6 = 33280, "Ausgang A6", 0, 100, PercentageUnit()
    OUTPUT_A7 = 33280, "Ausgang A7", 0, 100, PercentageUnit()
    OUTPUT_A8 = 33280, "Ausgang A8", 0, 100, PercentageUnit()
    OUTPUT_A9 = 33280, "Ausgang A9", 0, 100, PercentageUnit()
    OUTPUT_A10 = 33280, "Ausgang A10", 0, 100, PercentageUnit()
    OUTPUT_A11 = 33280, "Ausgang A11", 0, 100, PercentageUnit()
    OUTPUT_A12 = 33280, "Ausgang A12", 0, 100, PercentageUnit()
    OUTPUT_A13 = 33280, "Ausgang A13", 0, 100, PercentageUnit()
    OUTPUT_A14 = 33280, "Ausgang A14", 0, 100, PercentageUnit()

    ANALOG_OUT_O1 = 33294, "Analog Out O1", None, None, None # ToDo select: PWMUnit() / VoltUnit()
    ANALOG_OUT_O2 = 33295, "Analog Out O2", None, None, None # ToDo select: PWMUnit() / VoltUnit()
    ANALOG_OUT_O3 = 33296, "Analog Out O3", None, None, None # ToDo select: PWMUnit() / VoltUnit()
    ANALOG_OUT_O4 = 33297, "Analog Out O4", None, None, PWMUnit()   # WP Umwälzpumpe / Heat Pump Circulation Pump
    ANALOG_OUT_O5 = 33298, "Analog Out O5", None, None, None # ToDo select: PWMUnit() / VoltUnit()
    ANALOG_OUT_O6 = 33299, "Analog Out O6", None, None, None # ToDo select: PWMUnit() / VoltUnit()

    BURNER_STAGE_1_RUNTIME = 33536, "Laufzeit Brennerstufe 1", None, None, None
    BURNER_STAGE_1_STARTUPS = 33537, "Brennerstarts Stufe 1", None, None, None
    BURNER_STAGE_2_RUNTIME = 33538, "Laufzeit Brennerstufe 2", None, None, None

    HEAT_SOURCE_SX_CURRENT_POWER = 33539, "Wärmeerzeuger SX aktuelle Leistung", None, None, WattUnit()

    IONISATION_CURRENT = 33540, "Ionisationsstrom", None, None, AmpereUnit()

    MESSAGES_COUNT = 33792, "Meldungen Anzahl", None, None, None

    MESSAGE_1_CODE = 33793, "Meldung 1 Code", None, None, None
    MESSAGE_1_UNIX_TIME_H = 33794, "Meldung 1 UnixZeit H", None, None, None
    MESSAGE_1_UNIX_TIME_L = 33795, "Meldung 1 UnixZeit L", None, None, None
    MESSAGE_1_PARAMETER_1 = 33796, "Meldung 1 Par 1", None, None, None
    MESSAGE_1_PARAMETER_2 = 33797, "Meldung 1 Par 2", None, None, None
    MESSAGE_2_CODE = 33798, "Meldung 2 Code", None, None, None
    MESSAGE_2_UNIX_TIME_H = 33799, "Meldung 2 UnixZeit H", None, None, None
    MESSAGE_2_UNIX_TIME_L = 33800, "Meldung 2 UnixZeit L", None, None, None
    MESSAGE_2_PARAMETER_1 = 33801, "Meldung 2 Par 1", None, None, None
    MESSAGE_2_PARAMETER_2 = 33802, "Meldung 2 Par 2", None, None, None
    MESSAGE_3_CODE = 33803, "Meldung 3 Code", None, None, None
    MESSAGE_3_UNIX_TIME_H = 33804, "Meldung 3 UnixZeit H", None, None, None
    MESSAGE_3_UNIX_TIME_L = 33805, "Meldung 3 UnixZeit L", None, None, None
    MESSAGE_3_PARAMETER_1 = 33806, "Meldung 3 Par 1", None, None, None
    MESSAGE_3_PARAMETER_2 = 33807, "Meldung 3 Par 2", None, None, None
    MESSAGE_4_CODE = 33808, "Meldung 4 Code", None, None, None
    MESSAGE_4_UNIX_TIME_H = 33809, "Meldung 4 UnixZeit H", None, None, None
    MESSAGE_4_UNIX_TIME_L = 33810, "Meldung 4 UnixZeit L", None, None, None
    MESSAGE_4_PARAMETER_1 = 33811, "Meldung 4 Par 1", None, None, None
    MESSAGE_4_PARAMETER_2 = 33812, "Meldung 4 Par 2", None, None, None
    MESSAGE_5_CODE = 33813, "Meldung 5 Code", None, None, None
    MESSAGE_5_UNIX_TIME_H = 33814, "Meldung 5 UnixZeit H", None, None, None
    MESSAGE_5_UNIX_TIME_L = 33815, "Meldung 5 UnixZeit L", None, None, None
    MESSAGE_5_PARAMETER_1 = 33816, "Meldung 5 Par 1", None, None, None
    MESSAGE_5_PARAMETER_2 = 33817, "Meldung 5 Par 2", None, None, None
    MESSAGE_6_CODE = 33818, "Meldung 6 Code", None, None, None
    MESSAGE_6_UNIX_TIME_H = 33819, "Meldung 6 UnixZeit H", None, None, None
    MESSAGE_6_UNIX_TIME_L = 33820, "Meldung 6 UnixZeit L", None, None, None
    MESSAGE_6_PARAMETER_1 = 33821, "Meldung 6 Par 1", None, None, None
    MESSAGE_6_PARAMETER_2 = 33822, "Meldung 6 Par 2", None, None, None
    MESSAGE_7_CODE = 33823, "Meldung 7 Code", None, None, None
    MESSAGE_7_UNIX_TIME_H = 33824, "Meldung 7 UnixZeit H", None, None, None
    MESSAGE_7_UNIX_TIME_L = 33825, "Meldung 7 UnixZeit L", None, None, None
    MESSAGE_7_PARAMETER_1 = 33826, "Meldung 7 Par 1", None, None, None
    MESSAGE_7_PARAMETER_2 = 33827, "Meldung 7 Par 2", None, None, None
    MESSAGE_8_CODE = 33828, "Meldung 8 Code", None, None, None
    MESSAGE_8_UNIX_TIME_H = 33829, "Meldung 8 UnixZeit H", None, None, None
    MESSAGE_8_UNIX_TIME_L = 33830, "Meldung 8 UnixZeit L", None, None, None
    MESSAGE_8_PARAMETER_1 = 33831, "Meldung 8 Par 1", None, None, None
    MESSAGE_8_PARAMETER_2 = 33832, "Meldung 8 Par 2", None, None, None
    MESSAGE_9_CODE = 33833, "Meldung 9 Code", None, None, None
    MESSAGE_9_UNIX_TIME_H = 33834, "Meldung 9 UnixZeit H", None, None, None
    MESSAGE_9_UNIX_TIME_L = 33835, "Meldung 9 UnixZeit L", None, None, None
    MESSAGE_9_PARAMETER_1 = 33836, "Meldung 9 Par 1", None, None, None
    MESSAGE_9_PARAMETER_2 = 33837, "Meldung 9 Par 2", None, None, None
    MESSAGE_10_CODE = 33838, "Meldung 10 Code", None, None, None
    MESSAGE_10_UNIX_TIME_H = 33839, "Meldung 10 UnixZeit H", None, None, None
    MESSAGE_10_UNIX_TIME_L = 33840, "Meldung 10 UnixZeit L", None, None, None
    MESSAGE_10_PARAMETER_1 = 33841, "Meldung 10 Par 1", None, None, None
    MESSAGE_10_PARAMETER_2 = 33842, "Meldung 10 Par 2", None, None, None

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

    print(80*'#')
    print(ReadInputRegistersEnum.ANALOG_IN_1)
    print(ReadInputRegistersEnum.ANALOG_IN_1.value)
    print(ReadInputRegistersEnum.ANALOG_IN_1.address)
    ReadInputRegistersEnum.ANALOG_IN_1.value = 2
    print(ReadInputRegistersEnum.ANALOG_IN_1.value)
    print(ReadInputRegistersEnum.ANALOG_IN_1.unit)

    print(80*'#')
    print(ReadInputRegistersEnum.OUTPUT_A2)
    print(ReadInputRegistersEnum.OUTPUT_A2.value)
    print(ReadInputRegistersEnum.OUTPUT_A2.address)
    ReadInputRegistersEnum.OUTPUT_A2.value = 2
    print(ReadInputRegistersEnum.OUTPUT_A2.value)
    print(ReadInputRegistersEnum.OUTPUT_A2.unit)

    print(80*'#')
    print(ReadInputRegistersEnum.ANALOG_OUT_O4)
    print(ReadInputRegistersEnum.ANALOG_OUT_O4.value)
    print(ReadInputRegistersEnum.ANALOG_OUT_O4.address)
    ReadInputRegistersEnum.ANALOG_OUT_O4.value = 444
    print(ReadInputRegistersEnum.ANALOG_OUT_O4.value)
    print(ReadInputRegistersEnum.ANALOG_OUT_O4.unit)

    print(80*'#')
    print(ReadInputRegistersEnum.HEAT_SOURCE_SX_CURRENT_POWER)
    print(ReadInputRegistersEnum.HEAT_SOURCE_SX_CURRENT_POWER.value)
    print(ReadInputRegistersEnum.HEAT_SOURCE_SX_CURRENT_POWER.address)
    ReadInputRegistersEnum.HEAT_SOURCE_SX_CURRENT_POWER.value = 1
    print(ReadInputRegistersEnum.HEAT_SOURCE_SX_CURRENT_POWER.value)
    print(ReadInputRegistersEnum.HEAT_SOURCE_SX_CURRENT_POWER.unit)

    print(80*'#')
    print(ReadInputRegistersEnum.MESSAGE_8_CODE)
    print(ReadInputRegistersEnum.MESSAGE_8_CODE.value)
    print(ReadInputRegistersEnum.MESSAGE_8_CODE.address)
    ReadInputRegistersEnum.MESSAGE_8_CODE.value = 1
    print(ReadInputRegistersEnum.MESSAGE_8_CODE.value)
    print(ReadInputRegistersEnum.MESSAGE_8_CODE.unit)
