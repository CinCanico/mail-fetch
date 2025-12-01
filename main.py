import sys
import os
import configparser
import getpass
from typing import Tuple

from src.protocols.imap import fetch_imap
from src.protocols.pop3 import fetch_pop3


def main() -> None:
    # Load configuration
    server_address, port, protocol, timeout = try_read_config()

    # Get user credentials
    username = input("Enter Username: ").lstrip().rstrip()
    password = getpass.getpass("Enter Password: ")

    domain = '.'.join(server_address.split('.')[1:])
    email = f"{username}@{domain}"

    # Connect and Fetch directly
    if protocol == 'IMAP':
        fetch_imap(server_address, port, email,
                   password, timeout=timeout)
    elif protocol == 'POP3':
        fetch_pop3(server_address, port, email,
                   password, timeout=timeout)
    else:
        print(f"Error: Unsupported protocol {protocol}")


def try_read_config() -> Tuple[str, int, str, int]:
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        print("Error: config.ini not found.")
        sys.exit(1)

    config.read('config.ini')

    try:
        server_address = config['Server']['Address']
        port = int(config['Server']['Port'])
        protocol = config['Server']['Protocol'].upper()
        timeout = int(config['Server'].get('Timeout', 30))

    except KeyError as e:
        print(f"Error: Missing configuration key: {e}")
        sys.exit(1)
    except ValueError:
        print("Error: Port and Timeout must be integers.")
        sys.exit(1)
    return server_address, port, protocol, timeout


if __name__ == "__main__":
    main()
