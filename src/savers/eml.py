import os
from src.savers.base import SaverBase

class EmlSaver(SaverBase):
    def __init__(self, username: str, mailbox_name: str):
        super().__init__(username, mailbox_name)
        # Directory structure: backups/<username>/<inbox-name>/
        self.base_dir = os.path.join("backups", self.username_part, self.mailbox_name)
        os.makedirs(self.base_dir, exist_ok=True)

    def add(self, raw_email: bytes, identifier: str = ""):
        if not raw_email:
            return
        
        # Ensure identifier is safe for filename
        safe_identifier = "".join(c for c in identifier if c.isalnum() or c in ('-', '_', '.'))
        file_path = os.path.join(self.base_dir, f"{safe_identifier}.eml")
        
        with open(file_path, "wb") as f:
            f.write(raw_email)

    def close(self):
        pass
