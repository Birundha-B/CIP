import pika
import json
import smtplib
import time
import os

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from common.encryption import decrypt_message
from common.idempotency import is_duplicate, mark_processed
from orchestrator.orchestrator import orchestrate_email
from config.config import *


WORKER_ID = os.getpid()

start_time = None
processed_count = 0


def log(msg):
    print(f"[Worker {WORKER_ID}] {msg}", flush=True)



def send_email(receiver, subject, body, attachments=None):

    attachments = attachments or []

    for attempt in range(MAX_RETRIES):

        try:

            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = receiver
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            for file in attachments:

                part = MIMEBase("application", "octet-stream")
                part.set_payload(bytes.fromhex(file["data"]))

                encoders.encode_base64(part)

                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{file["filename"]}"'
                )

                msg.attach(part)

            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:

                server.login(EMAIL, APP_PASSWORD)
                server.send_message(msg)

            log("Email forwarded successfully")

            return True

        except Exception as e:

            log(f"Retry {attempt+1} failed: {e}")
            time.sleep(RETRY_DELAY)

    log("Email failed after retries")

    return False


# ==================================================
# PROCESS EMAIL
# ==================================================

def process_email(sender, subject, body, attachments):

    def send_wrapper(receiver, subject, body):

        success = send_email(
            receiver,
            subject,
            body,
            attachments
        )

        if not success:
            log("Email moved to failed queue")

        return success

    orchestrate_email(
        sender,
        subject,
        body,
        send_email_func=send_wrapper,
        log_func=log
    )


# ==================================================
# CALLBACK
# ==================================================

def callback(ch, method, properties, body):

    global start_time, processed_count

    try:

        if start_time is None:
            start_time = time.time()

        decrypted = decrypt_message(body)
        email_data = json.loads(decrypted)

        message_id = email_data["message_id"]

        if is_duplicate(message_id):
            log("Duplicate email skipped")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        sender = email_data["sender"]
        subject = email_data["subject"]

        log(f"Processing Email from {sender}")

        process_email(
            sender,
            subject,
            email_data["body"],
            email_data.get("attachments", [])
        )

        processed_count += 1

        mark_processed(message_id)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        log("Finished processing email")

        # ==================================================
        # PRINT TIMING
        # ==================================================

        elapsed = time.time() - start_time

        log(
            f"Processed {processed_count} emails "
            f"in {elapsed:.2f} seconds"
        )

    except Exception as e:
        log(f"Processing Error: {e}")


# ==================================================
# START WORKER
# ==================================================

def start_worker():

    while True:
        try:

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )

            channel = connection.channel()

            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue=RABBITMQ_QUEUE,
                on_message_callback=callback
            )

            log("Worker started...")

            channel.start_consuming()

        except Exception as e:
            log(f"Worker crashed: {e}")
            time.sleep(5)