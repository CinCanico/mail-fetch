from imaplib import IMAP4_SSL
import shlex
from typing import Optional
from src.mbox import MboxChunkManager


def connect_to_server(server: str, port: int, username: str, password: str, timeout: int = 30) -> IMAP4_SSL:
    """Connects to the IMAP server and logs in."""
    print(
        f"Connecting to IMAP server {server}:{port} with timeout {timeout}s...")
    mail = IMAP4_SSL(server, port, timeout=timeout)
    mail.login(username, password)
    return mail


def get_mailbox_list(mail: IMAP4_SSL) -> list[str]:
    """Lists all mailboxes."""
    print("Listing mailboxes...")
    status, mail_list = mail.list()
    if status != "OK":
        print("No mailboxes found!")
        return []
    if mail_list is None or type(mail_list) is not list:
        print("No mailboxes found!")
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


def search_emails(mail: IMAP4_SSL, mailbox_name: str) -> list[bytes]:
    """Selects a mailbox and searches for all emails."""
    print(f"Selecting mailbox: {mailbox_name}")
    status, _ = mail.select(f'"{mailbox_name}"') # Quote mailbox name
    if status != "OK":
        print(f"Failed to select mailbox {mailbox_name}")
        return []
        
    print(f"Searching for emails in {mailbox_name}...")
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print("No messages found!")
        return []
    # messages[0] is bytes, split returns list of bytes
    return messages[0].split()


def fetch_email(mail: IMAP4_SSL, email_id: bytes) -> Optional[bytes]:
    """Fetches a single email by ID."""
    status, msg_data = mail.fetch(email_id.decode(), "(RFC822)")
    if status == "OK" and msg_data[0] is not None:
        # msg_data[0] is a tuple (header, body) usually for RFC822
        # The body is at index 1 of the tuple
        if isinstance(msg_data[0], tuple):
             return msg_data[0][1]
    return None


def fetch_imap(server: str, port: int, username: str, password: str, mbox_path: str = 'backup.mbox', timeout: int = 30) -> None:
    """Orchestrates the IMAP fetch process."""
    try:
        mail = connect_to_server(server, port, username, password, timeout)
        mailbox_names = get_mailbox_list(mail)
        print(f"Mailboxes found: {mailbox_names}")

        for mb_name in mailbox_names:
            email_ids = search_emails(mail, mb_name)
            print(f"Found {len(email_ids)} emails in {mb_name}.")
            
            if not email_ids:
                continue

            with MboxChunkManager(username, mb_name) as manager:
                for email_id in email_ids:
                    raw_email = fetch_email(mail, email_id)
                    if raw_email:
                        manager.add(raw_email)
                
        mail.logout()
        print("Backup completed.")

    except Exception as e:
        print(f"An error occurred: {e}")
