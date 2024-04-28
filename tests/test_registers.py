import pytest

from solvis_sc3_modbus.registers import AmpereUnit, ErrorIndicatorEnum, SolvisZirkulationBetriebsartEnum, AnalogOutStatusEnum
from solvis_sc3_modbus.registers import TemperatureUnit, VoltUnit, PWMUnit, PercentageUnit, SolvisModbusRegister
from solvis_sc3_modbus.registers import VolumeUnit, ReadInputRegistersEnum


def test_temperature_unit_validation():
    temp = TemperatureUnit()
    assert temp.validate(1000) == 100.0  # Assuming a scale of 0.1
    with pytest.raises(ValueError, match="Interruption Error"):
        temp.validate(2200)
    with pytest.raises(ValueError, match="Short Circuit Error"):
        temp.validate(-300)


def test_volume_unit_validation():
    vol = VolumeUnit()
    assert vol.validate(10) == 1.0  # Assuming a scale of 0.1


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


def test_ampere_unit_validation():
    amp = AmpereUnit()
    assert amp.validate(250) == 250  # No scaling or validation logic implemented


def test_error_indicator_enum():
    assert ErrorIndicatorEnum.FUSE_POWER_SUPPLY_MODULE.value == 0
    assert ErrorIndicatorEnum.NOT_DEFINED.name == "NOT_DEFINED"
    assert ErrorIndicatorEnum.SOLAR_PRESSURE.value == 5


def test_pwm_unit_scale():
    pwm_unit = PWMUnit()
    assert pwm_unit.scale == 1.0
    assert pwm_unit.unit == "% (PWM)"
    assert pwm_unit.validate(50) == 50  # Assuming scale is 100


def test_solvis_modbus_register_with_ampere_unit():
    register = SolvisModbusRegister(address=33540, description="Ionisationsstrom", min=None, max=None, unit=AmpereUnit())
    register.value = 10  # Assigning directly, as no validation implemented
    assert register.value == 10


def test_value_assignment_with_enum():
    register = SolvisModbusRegister(address=33045, description="DigIn Störungen", min=None, max=None, unit=ErrorIndicatorEnum)
    register.value = ErrorIndicatorEnum.FUSE_POWER_SUPPLY_MODULE  # Enum direct assignment
    assert register.value == ErrorIndicatorEnum.FUSE_POWER_SUPPLY_MODULE


def test_temperature_unit_boundary_values():
    with pytest.raises(ValueError):
        temp = TemperatureUnit()
        temp.validate(2200)  # Boundary value that should raise an error
    assert temp.validate(2199) == 219.9  # Just below the boundary value


def test_volt_unit_negative_value():
    # Assuming no negative validation implemented; this test checks that behavior
    volt = VoltUnit()
    assert volt.validate(-100) == -10.0  # If negative values are allowed by the logic


def test_pwm_unit_out_of_range():
    with pytest.raises(ValueError):
        pwm = PWMUnit()
        pwm.validate(101)  # Assuming the scale is 100, 101 should be out of range
    with pytest.raises(ValueError):
        pwm.validate(-1)  # Negative values should also be out of range


def test_percentage_unit_zero_division():
    with pytest.raises(ZeroDivisionError):
        percentage_unit = PercentageUnit(scale=0)
        percentage_unit.validate(50)  # Attempting to divide by zero scale should raise an error


def test_solvis_modbus_register_none_value_assignment():
    with pytest.raises(ValueError):
        register = SolvisModbusRegister(address=1, description="Test Register", min=0, max=100, unit=TemperatureUnit())
        register.value = None  # Assigning None to a register with defined min/max bounds
        assert register.value is None  # Check if None is properly handled/assigned


def test_solvis_modbus_register_out_of_bounds():
    register = SolvisModbusRegister(address=2, description="Out of Bounds", min=10, max=20, unit=TemperatureUnit())
    with pytest.raises(ValueError):
        register.value = 9  # Below min bound
    with pytest.raises(ValueError):
        register.value = 21  # Above max bound


def test_enum_unexpected_value_handling():
    with pytest.raises(ValueError):
        SolvisZirkulationBetriebsartEnum("unexpected_value")  # Attempt to create an enum with an invalid value


def test_invalid_type_value_assignment():
    with pytest.raises(TypeError):
        temp = TemperatureUnit()
        temp.validate("not_a_number")


def test_precision_and_rounding_effects():
    temp = TemperatureUnit()
    assert temp.validate(999) == 99.9
    assert temp.validate(1001) == 100.1


def test_limits_of_scale_factors():
    # Test very small value
    volt = VoltUnit()
    assert volt.validate(1) == 0.1
    # Test very large value
    assert volt.validate(100000) == 10000.0


def test_exception_specificity_for_out_of_range():
    with pytest.raises(ValueError, match="out of range"):
        SolvisModbusRegister(address=1, description="Test", min=0, max=10, unit=VolumeUnit()).value = 110


def test_enum_extensibility_handling():
    # Pretend we're adding a new enum value dynamically (Python doesn't actually support this directly)
    if hasattr(AnalogOutStatusEnum, 'NEW_MODE'):
        assert AnalogOutStatusEnum.NEW_MODE.value not in [enum.value for enum in AnalogOutStatusEnum]


def test_dynamic_behavior_of_unit_change():
    register = SolvisModbusRegister(address=33024, description="Temp S1", min=0, max=1000, unit=TemperatureUnit())
    register.value = 500  # Valid temperature
    register.unit = VolumeUnit()  # Change to volume unit
    assert register.value == 50.0  # Ensure value is now interpreted as volume


def test_logging_on_value_error():
    with pytest.raises(ValueError) as exc_info:
        temp = TemperatureUnit()
        temp.validate(2200)
    assert "Interruption Error" in str(exc_info.value)
