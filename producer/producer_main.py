from producer.fetcher import fetch_loop
from message_queue.rabbitmq_setup import setup_rabbitmq


def main():
    print("Starting Producer...")

    setup_rabbitmq()
    fetch_loop()


if __name__ == "__main__":
    main()