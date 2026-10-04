import pika
from config.config import RABBITMQ_HOST, RABBITMQ_PORT


def setup_rabbitmq():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT
        )
    )

    channel = connection.channel()

    # ===============================
    # MAIN EXCHANGE
    # ===============================
    channel.exchange_declare(
        exchange="email_exchange",
        exchange_type="direct",
        durable=True
    )

    # ===============================
    # DLQ EXCHANGE
    # ===============================
    channel.exchange_declare(
        exchange="dlx_exchange",
        exchange_type="direct",
        durable=True
    )

    # ===============================
    # DEAD LETTER QUEUE
    # ===============================
    channel.queue_declare(
        queue="email_dlq",
        durable=True
    )

    channel.queue_bind(
        exchange="dlx_exchange",
        queue="email_dlq",
        routing_key="dlq"
    )

    # ===============================
    # MAIN QUEUE
    # ===============================
    args = {
        "x-dead-letter-exchange": "dlx_exchange",
        "x-dead-letter-routing-key": "dlq"
    }

    channel.queue_declare(
        queue="email_queue",
        durable=True,
        arguments=args
    )

    channel.queue_bind(
        exchange="email_exchange",
        queue="email_queue",
        routing_key="email"
    )

    print(" RabbitMQ setup completed successfully.")

    connection.close()


if __name__ == "__main__":
    setup_rabbitmq()