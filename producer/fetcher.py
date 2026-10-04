import email
import time
from email.header import decode_header

from producer.imap_oauth_client import connect_imap_oauth
from message_queue.rabbitmq import push_email

CHECK_INTERVAL = 5


def decode_subject(msg):

    subject = msg.get("Subject", "(No Subject)")
    decoded = decode_header(subject)

    result = ""
    for part, enc in decoded:
        if isinstance(part, bytes):
            result += part.decode(enc or "utf-8", errors="ignore")
        else:
            result += part

    return result


def extract_body_and_attachments(msg):

    body = ""
    attachments = []

    for part in msg.walk():

        content_type = part.get_content_type()
        disposition = str(part.get("Content-Disposition"))

        if content_type == "text/plain" and "attachment" not in disposition:
            payload = part.get_payload(decode=True)
            if payload:
                body += payload.decode(errors="ignore")

        if "attachment" in disposition:
            filename = part.get_filename()

            if filename:
                data = part.get_payload(decode=True)

                attachments.append({
                    "filename": filename,
                    "data": data.hex()
                })

    return body, attachments


def fetch_loop():

    print("IMAP Fetcher Started...")

    while True:
        try:
            imap = connect_imap_oauth()
            imap.select("INBOX")

            status, messages = imap.search(None, "UNSEEN")
            mail_ids = messages[0].split()

            for mail_id in mail_ids:

                _, msg_data = imap.fetch(mail_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                sender = msg.get("From")
                subject = decode_subject(msg)

                message_id = msg.get("Message-ID", str(mail_id))

                body, attachments = extract_body_and_attachments(msg)

                print("New Email:", subject)
                print("Attachments:", len(attachments))

                push_email(
                    sender,
                    subject,
                    body,
                    attachments,
                    message_id
                )

            imap.logout()

        except Exception as e:
            print("IMAP Error:", repr(e))

        time.sleep(CHECK_INTERVAL)