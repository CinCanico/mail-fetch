from poplib import POP3_SSL
from src.config import Config
from src.savers import get_saver

class POP3Protocol:
    def __init__(self, config: Config):
        self.config = config
        self.mail: POP3_SSL = self._connect()

    def _connect(self) -> POP3_SSL:
        """Connects to the POP3 server and logs in."""
        print(f"Connecting to POP3 server {self.config.server_address}:{self.config.port} with timeout {self.config.timeout}...")
        mail = POP3_SSL(self.config.server_address, self.config.port, timeout=self.config.timeout)
        try:
            mail.user(self.config.email)
            mail.pass_(self.config.password)
        except Exception as e:
            print(f"Login with username '{self.config.email}' failed: {e}")
            if self.config.username and self.config.username != self.config.email:
                print(f"Retrying login with username '{self.config.username}'...")
                try:
                    mail = POP3_SSL(self.config.server_address, self.config.port, timeout=self.config.timeout)
                    mail.user(self.config.username)
                    mail.pass_(self.config.password)
                except Exception as e2:
                    print(f"Login with username '{self.config.username}' failed: {e2}")
                    raise e
            else:
                raise e
        return mail

    def get_email_count(self) -> int:
        """Returns the number of messages."""
        return len(self.mail.list()[1])

    def fetch_email(self, index: int) -> bytes:
        """Fetches a single email by index."""
        print(f"Fetching email {index}...")
        # retr returns (response, lines, octets)
        response, lines, octets = self.mail.retr(index)
        return b"\n".join(lines)

    def run(self) -> None:
        """Orchestrates the POP3 fetch process."""
        try:
            num_messages = self.get_email_count()
            print(f"Found {num_messages} emails.")

            # POP3 only has INBOX usually
            with get_saver(self.config.file_type, self.config.username, "INBOX", self.config.max_file_size) as saver:
                for i in range(num_messages):
                    raw_email = self.fetch_email(i+1)
                    saver.add(raw_email, str(i+1))

            self.mail.quit()
            print("Backup completed.")

        except Exception as e:
            print(f"An error occurred: {e}")
