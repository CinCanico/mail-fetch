from enum import Enum

class Protocol(Enum):
    IMAP = "IMAP"
    POP3 = "POP3"

    # Return the value of the enum automatically in match statements
    def __str__(self):
        return self.value

