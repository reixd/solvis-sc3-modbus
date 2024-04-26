#!/usr/bin/env python3

import os
from solvis_sc3_modbus.log_config import setup_logging
from solvis_sc3_modbus.client import SolvisSC3ModbusClient

logger = setup_logging("SolvisSC3")


# Use environment variables for host and port configuration
host = os.getenv('SOLVIS_HOST', 'localhost')
port = int(os.getenv('SOLVIS_PORT', 502))
unit_id = int(os.getenv('SOLVIS_UNIT_ID', 101))
register_address = int(os.getenv('SOLVIS_REG_ADDRESS', -1))
register_name = os.getenv('SOLVIS_REG_NAME')


def main():
    solvis_client = SolvisSC3ModbusClient(host=host, port=port, unit_id=unit_id, debug=False)
    if solvis_client.connect():
        if register_address != -1:
            data = solvis_client.fetch_data(register_address=register_address, length=1)
        elif register_name is None:
            data = solvis_client.get_TEMP_S1  # This will call fetch_data(33024)
        elif register_name:
            data = solvis_client.get(register_name)
        else:
            raise Exception("No register_name or register_address specified.")
        logger.info(f"Data from registers: {data}")
    else:
        logger.error("Connection to Solvis SC3 device failed.")


if __name__ == "__main__":
    main()
