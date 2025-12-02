import configparser
import os
import sys
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    # Server Configuration: 
    server_address: str
    port: int
    protocol: str
    timeout: int
    username: str = ""
    password: str = field(default="", repr=False)
    
    @property
    def email(self) -> str:
        if not self.username or not self.server_address:
            return ""
        domain = '.'.join(self.server_address.split('.')[1:])
        return f"{self.username}@{domain}"
    
    # Backup Configuration: 
    max_file_size: int = 128 * 1024 * 1024



class ConfigManager:
    def __init__(self):
        self.config: Optional[Config] = None

    def load_config(self, config_path: str = 'config.ini') -> Config:
        config_parser = configparser.ConfigParser()
        if not os.path.exists(config_path):
            print(f"Error: {config_path} not found.")
            sys.exit(1)

        config_parser.read(config_path)

        try:
            server_address = config_parser['Server']['Address']
            port = int(config_parser['Server'].get('Port', 993))
            protocol = config_parser['Server']['Protocol'].upper()
            timeout = int(config_parser['Server'].get('Timeout', 30))

            max_file_size = int(config_parser['Backup'].get(
                'MaxFileSize', 128)) * 1024 * 1024

            self.config = Config(
                server_address=server_address,
                port=port,
                protocol=protocol,
                timeout=timeout,
                max_file_size=max_file_size
            )
            return self.config

        except KeyError as e:
            print(f"Error: Missing configuration key: {e}")
            sys.exit(1)
        except ValueError as e:
            print(
                f"Error: Port, Timeout and MaxFileSize must be integers. {e}")
            sys.exit(1)

    def set_credentials(self, username: str, password: str) -> None:
        if self.config:
            self.config.username = username
            self.config.password = password
