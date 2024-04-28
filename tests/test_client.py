import unittest
from unittest.mock import patch, MagicMock

from solvis_sc3_modbus.client import SolvisSC3ModbusClient
from solvis_sc3_modbus.registers import ReadInputRegistersEnum


class TestSolvisSC3ModbusClientMore(unittest.TestCase):

    def setUp(self):
        self.host = "192.168.1.100"
        self.port = 502
        self.unit_id = 1

        # Patching the ModbusClient to not actually attempt network connections
        self.modbus_client_patcher = patch('solvis_sc3_modbus.client.ModbusClient')
        self.MockModbusClient = self.modbus_client_patcher.start()
        self.mock_client_instance = self.MockModbusClient.return_value

        # Patching logger to prevent actual logging during tests
        self.logger_patcher = patch('solvis_sc3_modbus.client.logger')
        self.mock_logger = self.logger_patcher.start()

    def tearDown(self):
        self.modbus_client_patcher.stop()
        self.logger_patcher.stop()

    def test_get_register_value_success(self):
        # Setup mock return value for fetch_data
        register_name = 'TEMP_S1'
        original_value = 420
        expected_value = 42.0
        expected_unit = "°C"
        self.mock_client_instance.read_holding_registers.return_value = [original_value]

        modbus_client = SolvisSC3ModbusClient(self.host, self.port, self.unit_id)
        result_value, result_unit = modbus_client.get(register_name)

        self.assertEqual(expected_value, result_value)
        self.assertEqual(expected_unit, result_unit)

    def test_get_attribute_dynamic_access(self):
        # Testing dynamic attribute access for getting register values through get_<register_name> methods
        register_name = 'TEMP_S1'
        original_value = 420
        expected_value = 42.0
        self.mock_client_instance.read_holding_registers.return_value = [original_value]

        modbus_client = SolvisSC3ModbusClient(self.host, self.port, self.unit_id)
        result = modbus_client.get_TEMP_S1

        self.assertEqual(expected_value, result[0])  # Validate returned value matches expected

    def test_get_register_value_invalid_register(self):
        # Attempt to get a value for a non-existent register
        register_name = 'INVALID_REGISTER'
        modbus_client = SolvisSC3ModbusClient(self.host, self.port, self.unit_id)

        with self.assertRaises(AttributeError):
            _, _ = modbus_client.get(register_name)


if __name__ == '__main__':
    unittest.main()
