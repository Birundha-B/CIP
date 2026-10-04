import pika
import json
import time

from common.encryption import encrypt_message
from config.config import RABBITMQ_HOST, RABBITMQ_PORT


connection = None
channel = None


# ==================================================
# SAFE RABBITMQ CONNECTION
# ==================================================
def connect_rabbit():

    global connection, channel

    while True:
        try:
            print(" Connecting to RabbitMQ...")

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )

            channel = connection.channel()

            print(" RabbitMQ Connected")
            break

        except Exception as e:
            print("⚠ RabbitMQ not ready... retrying in 5 sec")
            time.sleep(5)


# connect at startup
connect_rabbit()


# ==================================================
# ENSURE CONNECTION
# ==================================================
def ensure_connection():

    global connection, channel

    if (
        connection is None
        or connection.is_closed
        or channel is None
        or channel.is_closed
    ):
        print("♻ Reconnecting RabbitMQ...")
        connect_rabbit()


# ==================================================
# PUSH EMAIL TO QUEUE
# ==================================================
def push_email(sender, subject, body, attachments, message_id):

    global channel

    try:
        ensure_connection()

        email_data = {
            "message_id": message_id,
            "sender": sender,
            "subject": subject,
            "body": body,
            "attachments": attachments
        }

        encrypted = encrypt_message(
            json.dumps(email_data)
        )

        channel.basic_publish(
            exchange="email_exchange",
            routing_key="email",
            body=encrypted,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

        print("\nEMAIL PUSHED TO QUEUE")
        print(f"From    : {sender}")
        print(f"Subject : {subject}")
        print("================================")

    except Exception as e:
        print(" Push Failed:", e)
        connect_rabbit()