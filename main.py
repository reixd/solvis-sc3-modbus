#!/usr/bin/env python3

import os
from solvis_sc3_modbus.client import SolvisSC3ModbusClient

# Use environment variables for host and port configuration
host = os.getenv('SOLVIS_HOST', 'localhost')
port = int(os.getenv('SOLVIS_PORT', 502))
unit_id = int(os.getenv('SOLVIS_UNIT_ID', 101))
register_address = int(os.getenv('SOLVIS_REG_ADDRESS', 33024))


def main():
    solvis_client = SolvisSC3ModbusClient(host=host, port=port, unit_id=unit_id, debug=False)
    if solvis_client.connect():
        data = solvis_client.fetch_data(register_address=register_address, length=1)
        print("Data from registers:", data)
    else:
        print("Connection to Solvis SC3 device failed.")


if __name__ == "__main__":
    main()
