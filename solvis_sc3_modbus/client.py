from pyModbusTCP.client import ModbusClient

from solvis_sc3_modbus.log_config import setup_logging
from solvis_sc3_modbus.registers import ReadInputRegistersEnum

logger = setup_logging("SolvisSC3ModbusClient")


class SolvisSC3ModbusClient(object):
    def __init__(self, host, port, unit_id=1, debug=False):
        self.host = host
        self.port = port
        self.client = ModbusClient(host=self.host, port=self.port, unit_id=unit_id, debug=debug, auto_open=True)

    def __getattr__(self, attr):
        if attr.startswith("get_"):
            _register_name = attr.split('_', 1)[1:][0].upper()  # Remove 'fetch_' prefix and convert to uppercase
            try:
                _register = ReadInputRegistersEnum[_register_name]
                _register.value = self.get(_register.address)
                return _register.value, _register.unit.unit
            except KeyError:
                raise AttributeError(f"No matching enum member found for {attr}")
        else:
            # Fallback for other undefined attributes
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")

    def connect(self):
        if self.client.open():
            logger.info("Connected to Solvis SC3 device.")
            return True
        else:
            logger.error("Failed to connect to Solvis SC3 device.")
            return False

    def get(self, register_address, length=1):
        """
        Fetch data from a specific register.

        Args:
            register_address (int): The address of the register to read from.
            length (int): Number of registers to read.

        Returns:
            list or int: A single register value or a list of register values, or None if failed.
        """
        # Attempt to connect if client is not already open. Return None immediately upon failure.
        if not self.client.is_open and not self.connect():
            logger.error("Cannot fetch data. Connection to Solvis SC3 device failed.")
            return None

        try:
            data = self.client.read_holding_registers(register_address, length)
            if data is None:
                logger.warning(f"Failed to fetch data from register {register_address}.")
                return None
            else:
                logger.info(f"Data fetched from register {register_address}: {data}")
                # Simplify return statement
                return data[0] if length == 1 else data
        except Exception as e:
            logger.error(f"Exception while fetching data: {e}")
            return None
