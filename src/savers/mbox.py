import os
import mailbox
from typing import Optional
from src.savers.base import SaverBase


class MboxSaver(SaverBase):
    def __init__(self, username: str, mailbox_name: str, max_size_bytes: int = 128 * 1024 * 1024):
        super().__init__(username, mailbox_name)
        self.max_size = max_size_bytes
        self.chunk = 1
        self.current_mbox: Optional[mailbox.mbox] = None
        self.current_path = ""
        self.current_size = 0

        # Ensure backup directory exists
        os.makedirs("backups", exist_ok=True)

        self._open_mbox()

    def _get_filename(self) -> str:
        return os.path.join("backups", f"{self.username_part}.{self.mailbox_name}.{self.chunk}.mbox")

    def _open_mbox(self):
        self.current_path = self._get_filename()
        while os.path.exists(self.current_path) and os.path.getsize(self.current_path) >= self.max_size:
            self.chunk += 1
            self.current_path = self._get_filename()

        if os.path.exists(self.current_path):
            self.current_size = os.path.getsize(self.current_path)
        else:
            self.current_size = 0

        self.current_mbox = mailbox.mbox(self.current_path)
        self.current_mbox.lock()

    def add(self, raw_email: bytes, identifier: str = ""):
        if not raw_email:
            return

        # Check if adding this email would exceed the max size
        # We use len(raw_email) which returns the number of bytes in the bytes object.
        # This is accurate for the payload size. Mbox adds a small overhead ("From " line),
        # but for splitting purposes, this is sufficient.
        next_size = (self.current_size + len(raw_email))
        if self.current_size > 0 and next_size > self.max_size:
            self.close()
            self.chunk += 1
            self._open_mbox()

        if self.current_mbox is not None:
            self.current_mbox.add(raw_email)
            self.current_mbox.flush()
            # Update current size
            self.current_size += len(raw_email)

    def close(self):
        if self.current_mbox is not None:
            try:
                self.current_mbox.flush()
            except Exception as e:
                print(f"Error flushing mbox: {e}")
            finally:
                try:
                    self.current_mbox.unlock()
                except Exception as e:
                    print(f"Error unlocking mbox: {e}")
                finally:
                    self.current_mbox.close()
                    self.current_mbox = None
                    self.current_size = 0

