from typing import Union, TYPE_CHECKING
from src.enums import Protocol
from src.protocols.imap import IMAPProtocol
from src.protocols.pop3 import POP3Protocol

if TYPE_CHECKING:
    from src.config import Config


def get_protocol(config: 'Config') -> Union[IMAPProtocol, POP3Protocol]:
    match config.protocol:
        case Protocol.IMAP:
            return IMAPProtocol(config)
        case Protocol.POP3:
            return POP3Protocol(config)
        case _:
            raise ValueError(f"Unsupported protocol: {config.protocol}")
