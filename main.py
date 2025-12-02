import sys
import os

import getpass


from src.protocols import Protocol
from src.protocols.imap import fetch_imap
from src.protocols.pop3 import fetch_pop3
from src.config import ConfigManager


def main() -> None:
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Get user credentials
    username = input("Enter Username: ").lstrip().rstrip()
    password = getpass.getpass("Enter Password: ")

    config_manager.set_credentials(username, password)

    if len(config.username) == 0 or len(config.password) == 0:
        print("Error: Username and Password are required.")
        return
    print(f"{config}")
    
    # Connect and Fetch directly
    match config.protocol:
        case Protocol.IMAP.value:
            fetch_imap(config)
        case Protocol.POP3.value:
            fetch_pop3(config.server_address, config.port, config.email,
                       config.password, timeout=config.timeout)
        case _:
            print(f"Error: Unsupported protocol {config.protocol}")


if __name__ == "__main__":
    main()
