from enum import Enum

class Protocol(Enum):
    IMAP = "IMAP"
    POP3 = "POP3"

    def __str__(self):
        return self.value

class Saver(Enum):
    EML = "EML"
    MBOX = "MBOX"

def get_protocol_enum(protocol: str) -> Protocol:
    match protocol:
        case Protocol.IMAP.value:
            return Protocol.IMAP
        case Protocol.POP3.value:
            return Protocol.POP3
        case _:
            raise ValueError(f"Unsupported protocol: {protocol}")

def get_saver_enum(file_type: str) -> Saver:
    match file_type.upper():
        case Saver.MBOX.value:
            return Saver.MBOX
        case Saver.EML.value:
            return Saver.EML
        case _:
            raise ValueError(f"Unsupported file type: {file_type}")
