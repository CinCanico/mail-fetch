# Mail Fetch

Mail Fetch is a Python script that fetches all emails associated with the given username and password from a POP3 or IMAP server and backup the emails to a local directory in Mbox or EML format. IMAP is recommended.

## Usage

1. Set up your `config.ini` file then in your terminal:
2. Start the application
   ```bash
   python3 main.py
   ```
3. Write your username and password.
   > Username is used with the Address line in config. Part before the first dot (".") on the Address line is removed and added with username such that the final email is \<username>@\<address-after-first-dot>. Example : Address is mail.url.com and username is info. Resulting email is info@url.com
