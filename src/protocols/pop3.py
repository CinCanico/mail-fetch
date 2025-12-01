from poplib import POP3_SSL
from src.mbox import MboxChunkManager

def connect_to_server(server: str, port: int, username: str, password: str, timeout: int = 30) -> POP3_SSL:
    """Connects to the POP3 server and logs in."""
    print(f"Connecting to POP3 server {server}:{port} with timeout {timeout}...")
    mail = POP3_SSL(server, port, timeout=timeout)
    mail.user(username)
    mail.pass_(password)
    return mail

def get_email_count(mail: POP3_SSL) -> int:
    """Returns the number of messages."""
    return len(mail.list()[1])

def fetch_email(mail: POP3_SSL, index: int) -> bytes:
    """Fetches a single email by index."""
    print(f"Fetching email {index}...")
    # retr returns (response, lines, octets)
    response, lines, octets = mail.retr(index)
    return b"\n".join(lines)

def fetch_pop3(server: str, port: int, username: str, password: str, mbox_path: str = 'backup.mbox', timeout: int = 30) -> None:
    """Orchestrates the POP3 fetch process."""
    try:
        mail = connect_to_server(server, port, username, password, timeout)
        print(mail.list())
        num_messages = get_email_count(mail)
        print(f"Found {num_messages} emails.")

        # POP3 only has INBOX usually
        with MboxChunkManager(username, "INBOX") as manager:
            for i in range(num_messages):
                raw_email = fetch_email(mail, i+1)
                manager.add(raw_email)

        mail.quit()
        print("Backup completed.")

    except Exception as e:
        print(f"An error occurred: {e}")
