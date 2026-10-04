from imap_oauth_client import connect_imap_oauth
import email

EMAIL = "cipprojectmain@gmail.com"

imap = None

try:
    imap = connect_imap_oauth(EMAIL)
    imap.select("INBOX")

    status, messages = imap.search(None, "UNSEEN")
    mail_ids = messages[0].split()

    print("Unread messages:", mail_ids)

    for mail_id in mail_ids:
        status, msg_data = imap.fetch(mail_id, "(RFC822)")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"]
        sender = msg["from"]

        print("\n--- Email ---")
        print("From:", sender)
        print("Subject:", subject)

        # Get body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    print("Body:", body[:200])  # first 200 chars
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
            print("Body:", body[:200])

except Exception as e:
    print("Error:", e)

finally:
    if imap:
        try:
            imap.logout()
        except:
            pass
