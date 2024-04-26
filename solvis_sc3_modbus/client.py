from pyModbusTCP.client import ModbusClient

from solvis_sc3_modbus.log_config import setup_logging

logger = setup_logging()


class SolvisSC3ModbusClient(object):
    def __init__(self, host, port, unit_id=1, debug=False):
        self.host = host
        self.port = port
        self.client = ModbusClient(host=self.host, port=self.port, unit_id=unit_id, debug=debug, auto_open=True)

    def connect(self):
        if self.client.open():
            logger.info("Connected to Solvis SC3 device.")
            return True
        else:
            logger.error("Failed to connect to Solvis SC3 device.")
            return False

    def fetch_data(self, register_address, length=1):
        """
        Fetch data from a specific register.

        Args:
            register_address (int): The address of the register to read from.
            length (int): Number of registers to read.

        Returns:
            list: Register values or None if failed.
        """
        if not self.client.is_open:
            if not self.connect():
                logger.error("Cannot fetch data. Connection to Solvis SC3 device failed.")
                return None
        data = self.client.read_holding_registers(register_address, length)
        if data is not None:
            logger.info(f"Data fetched from register {register_address}: {data}")
        else:
            logger.warning(f"Failed to fetch data from register {register_address}.")
        return data
