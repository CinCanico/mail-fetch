from imaplib import IMAP4_SSL
import shlex
from typing import Optional
from src.config import Config
from src.savers import get_saver


class IMAPProtocol:
    def __init__(self, config: Config):
        self.config = config
        self.mail: Optional[IMAP4_SSL] = None

    def _connect(self) -> IMAP4_SSL:
        """Connects to the IMAP server and logs in."""
        print(
            f"Connecting to IMAP server {self.config.server_address}:{self.config.port} with timeout {self.config.timeout}s...")
        mail = IMAP4_SSL(self.config.server_address,
                         self.config.port, timeout=self.config.timeout)
        try:
            mail.login(self.config.email, self.config.password)
        except mail.error as e:
            print(f"Login with username '{self.config.email}' failed: {e}")
            if self.config.username and self.config.username != self.config.email:
                print(
                    f"Retrying login with username '{self.config.username}'...")
                try:
                    mail.login(self.config.username, self.config.password)
                except mail.error as e2:
                    print(
                        f"Login with username '{self.config.username}' failed: {e2}")
                    raise e
            else:
                raise e
        return mail

    @property
    def _safe_mail(self) -> IMAP4_SSL:
        if self.mail is None:
            raise ConnectionError("IMAP connection not established")
        return self.mail

    def get_mailbox_list(self) -> list[str]:
        """Lists all mailboxes."""
        print(f"{self.config.email:20}: Listing mailboxes...")
        status, mail_list = self._safe_mail.list()
        if status != "OK":
            print(f"{self.config.email:20}: No mailboxes found!")
            return []
        if mail_list is None or type(mail_list) is not list:
            print(f"{self.config.email:20}: No mailboxes found!")
            return []

        mailboxes = []
        for listitem in mail_list:
            if type(listitem) is not bytes:
                continue
            # Parse the mailbox name from the response
            # Response format: b'(\\HasNoChildren) "/" "INBOX"'
            decoded = listitem.decode('utf-8')
            # Simple parsing: assume the last quoted string is the mailbox name
            # Using shlex to handle quotes properly
            try:
                parts = shlex.split(decoded)
                if parts:
                    mailboxes.append(parts[-1])
            except ValueError:
                print(f"Failed to parse mailbox name: {decoded}")

        return mailboxes

    def search_emails(self, mailbox_name: str) -> list[bytes]:
        """Selects a mailbox and searches for all emails."""
        print(f"{self.config.email:20}: {mailbox_name:20}: Selected")
        status, _ = self._safe_mail.select(
            f'"{mailbox_name}"')  # Quote mailbox name
        if status != "OK":
            print(f"Failed to select mailbox {mailbox_name}")
            return []

        print(f"{self.config.email:20}: {mailbox_name:20}: Searching...")
        status, messages = self._safe_mail.search(None, "ALL")
        if status != "OK":
            print("No messages found!")
            return []
        # messages[0] is bytes, split returns list of bytes
        return messages[0].split()

    def fetch_email(self, email_id: bytes, mb_name: str) -> Optional[bytes]:
        """Fetches a single email by ID."""
        print(f"{self.config.email:20}: {mb_name:20}: Fetching {email_id.decode()}")
        status, msg_data = self._safe_mail.fetch(email_id.decode(), "(RFC822)")
        if status == "OK" and msg_data[0] is not None:
            # msg_data[0] is a tuple (header, body) usually for RFC822
            # The body is at index 1 of the tuple
            if isinstance(msg_data[0], tuple):
                return msg_data[0][1]
        return None

    def run(self) -> None:
        """Orchestrates the IMAP fetch process."""
        try:
            self.mail = self._connect()
            if self.mail is None:
                raise ConnectionError(
                    "Failed to establish connection to IMAP server.")

            mailbox_names = self.get_mailbox_list()
            print(f"{"Mailboxes found":20}: {mailbox_names}")

            for mb_name in mailbox_names:
                email_ids = self.search_emails(mb_name)
                print(
                    f"{self.config.email:20}: {mb_name:20}: {len(email_ids)} emails found.")

                if not email_ids:
                    continue

                with get_saver(self.config.file_type, self.config.username, mb_name, self.config.max_file_size) as saver:
                    for email_id in email_ids:
                        raw_email = self.fetch_email(email_id, mb_name)
                        if raw_email:
                            saver.add(raw_email, email_id.decode())

            self.mail.logout()
            print("Backup completed.")

        except Exception as e:
            print(f"An error occurred: {e}")
