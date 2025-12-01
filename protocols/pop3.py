import mailbox
import poplib

def connect_to_server(server, port, username, password):
    """Connects to the POP3 server and logs in."""
    print(f"Connecting to POP3 server {server}:{port}...")
    mail = poplib.POP3_SSL(server, port)
    mail.user(username)
    mail.pass_(password)
    return mail

def get_email_count(mail):
    """Returns the number of messages."""
    return len(mail.list()[1])

def fetch_email(mail, index):
    """Fetches a single email by index."""
    print(f"Fetching email {index}...")
    # retr returns (response, lines, octets)
    response, lines, octets = mail.retr(index)
    return b"\n".join(lines)

def save_to_mbox(mbox, raw_email):
    """Saves a single email to the mbox file."""
    if raw_email:
        mbox.add(raw_email)

def fetch_pop3(server, port, username, password, mbox_path='backup.mbox'):
    """Orchestrates the POP3 fetch process."""
    try:
        mail = connect_to_server(server, port, username, password)

        num_messages = get_email_count(mail)
        print(f"Found {num_messages} emails.")

        mbox = mailbox.mbox(mbox_path)
        mbox.lock()

        try:
            for i in range(num_messages):
                raw_email = fetch_email(mail, i+1)
                save_to_mbox(mbox, raw_email)
        finally:
            mbox.flush()
            mbox.unlock()
            mbox.close()
            mail.quit()
            print("Backup completed.")

    except Exception as e:
        print(f"An error occurred: {e}")
