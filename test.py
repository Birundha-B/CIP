

import smtplib
import time
from email.mime.text import MIMEText

# Sender Email
EMAIL = "birundhabs26@gmail.com"
APP_PASSWORD = "elckpawlhgpzdpng"

# Receiver (your project email)
RECEIVER = "cipprojectmain@gmail.com"

# Number of emails
NUM_EMAILS = 25


def send_bulk_emails():

    start_time = time.time()

    try:
        # Open single connection
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, APP_PASSWORD)

        for i in range(NUM_EMAILS):

            msg = MIMEText(f"Load test email {i}")
            msg["Subject"] = f"Load Test {i}"
            msg["From"] = EMAIL
            msg["To"] = RECEIVER

            try:
                server.send_message(msg)
                print(f"Sent Email {i}")

            except Exception as e:
                print(f"Failed Email {i}: {e}")

            # small delay to avoid blocking
            time.sleep(0.2)

        server.quit()

    except Exception as e:
        print("Connection Error:", e)

    end_time = time.time()

    print("\nTotal Emails Sent:", NUM_EMAILS)
    print("Time Taken:", end_time - start_time)


if __name__ == "__main__":
    send_bulk_emails()