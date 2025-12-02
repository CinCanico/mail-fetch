from abc import ABC, abstractmethod

class SaverBase(ABC):
    def __init__(self, username: str, mailbox_name: str):
        self.username_part = username.split('@')[0]
        self.mailbox_name = mailbox_name

    @abstractmethod
    def add(self, raw_email: bytes, identifier: str = ""):
        pass
    
    @abstractmethod
    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
