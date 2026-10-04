import imaplib
import email
from email.header import decode_header

from config.config import EMAIL
from token_manager import get_access_token


def connect_imap():

    access_token = get_access_token()
    print("Access token obtained.")

    auth_string = f"user={EMAIL}\x01auth=Bearer {access_token}\x01\x01"

    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    imap.authenticate("XOAUTH2", lambda x: auth_string)

    return imap


def fetch_unread_emails():

    imap = connect_imap()

    imap.select("INBOX")

    status, messages = imap.search(None, "UNSEEN")

    mail_ids = messages[0].split()

    print(f"Unread Emails: {len(mail_ids)}")

    for mail_id in mail_ids:

        status, msg_data = imap.fetch(mail_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):

                msg = email.message_from_bytes(response_part[1])

                subject, encoding = decode_header(
                    msg["Subject"]
                )[0]

                if isinstance(subject, bytes):
                    subject = subject.decode(
                        encoding if encoding else "utf-8"
                    )

                print("\n======================")
                print("Subject:", subject)

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(
                                decode=True
                            ).decode(errors="ignore")
                            print("Body:", body[:300])
                            break
                else:
                    body = msg.get_payload(
                        decode=True
                    ).decode(errors="ignore")
                    print("Body:", body[:300])

    imap.logout()


if __name__ == "__main__":
    fetch_unread_emails()