import pytest

from solvis_sc3_modbus.registers import TemperatureUnit, VolumeUnit, SolvisModbusRegister, ReadInputRegistersEnum


def test_temperature_unit_validation():
    assert TemperatureUnit.validate(1000) == 100.0  # Assuming a scale of 0.1
    with pytest.raises(ValueError, match="Interruption Error"):
        TemperatureUnit.validate(2200)
    with pytest.raises(ValueError, match="Short Circuit Error"):
        TemperatureUnit.validate(-300)


def test_volume_unit_validation():
    assert VolumeUnit.validate(10) == 1.0  # Assuming a scale of 0.1


def test_solvis_modbus_register_value_assignment():
    register = SolvisModbusRegister(address=33024, description="Temp S1", min=0, max=4200, unit=TemperatureUnit())
    register.value = 420  # Valid value
    assert register.value == 42.0  # Assuming a scale of 0.1
    with pytest.raises(ValueError):
        register.value = 4300  # Out of range


def test_enum_functionality():
    assert ReadInputRegistersEnum.TEMP_S1.unit.unit == "°C"
    assert ReadInputRegistersEnum.TEMP_S1.address == 33024
    assert isinstance(ReadInputRegistersEnum.VOLUME_FLOW_S17.unit, VolumeUnit)
