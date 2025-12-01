import configparser
import getpass
import os
import sys
from protocols.imap import fetch_imap
from protocols.pop3 import fetch_pop3

def main():
    # Load configuration
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        print("Error: config.ini not found.")
        return

    config.read('config.ini')
    
    try:
        server_address = config['Server']['Address']
        port = int(config['Server']['Port'])
        protocol = config['Server']['Protocol'].upper()
    except KeyError as e:
        print(f"Error: Missing configuration key: {e}")
        return
    except ValueError:
        print("Error: Port must be an integer.")
        return

    # Get user credentials
    username = input("Enter Username (email): ")
    password = getpass.getpass("Enter Password: ")

    # Connect and Fetch
    if protocol == 'IMAP':
        fetch_imap(server_address, port, username, password)
    elif protocol == 'POP3':
        fetch_pop3(server_address, port, username, password)
    else:
        print(f"Error: Unsupported protocol {protocol}")

if __name__ == "__main__":
    main()
