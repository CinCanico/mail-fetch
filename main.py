from src.protocols import get_protocol
import getpass

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
    protocol = get_protocol(config)
    protocol.run()


if __name__ == "__main__":
    main()
