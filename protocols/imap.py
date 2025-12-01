import imaplib
import mailbox

def connect_to_server(server, port, username, password):
    """Connects to the IMAP server and logs in."""
    print(f"Connecting to IMAP server {server}:{port}...")
    mail = imaplib.IMAP4_SSL(server, port)
    mail.login(username, password)
    return mail

def search_emails(mail):
    """Selects INBOX and searches for all emails."""
    mail.select("INBOX")
    print("Searching for emails...")
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print("No messages found!")
        return []
    return messages[0].split()

def fetch_email(mail, email_id):
    """Fetches a single email by ID."""
    print(f"Fetching email {email_id.decode()}...")
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    if status == "OK":
        # msg_data[0] is a tuple (header, body) usually for RFC822
        return msg_data[0][1]
    return None

def save_to_mbox(mbox, raw_email):
    """Saves a single email to the mbox file."""
    if raw_email:
        mbox.add(raw_email)

def fetch_imap(server, port, username, password, mbox_path='backup.mbox'):
    """Orchestrates the IMAP fetch process."""
    try:
        mail = connect_to_server(server, port, username, password)
        
        email_ids = search_emails(mail)
        print(f"Found {len(email_ids)} emails.")

        mbox = mailbox.mbox(mbox_path)
        mbox.lock()

        try:
            for email_id in email_ids:
                raw_email = fetch_email(mail, email_id)
                save_to_mbox(mbox, raw_email)
        finally:
            mbox.flush()
            mbox.unlock()
            mbox.close()
            mail.logout()
            print("Backup completed.")

    except Exception as e:
        print(f"An error occurred: {e}")
