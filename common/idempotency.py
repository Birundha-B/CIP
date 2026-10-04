import os

PROCESSED_FILE = "processed_ids.txt"


def is_duplicate(message_id):

    if not os.path.exists(PROCESSED_FILE):
        return False

    with open(PROCESSED_FILE, "r") as f:
        ids = f.read().splitlines()

    return message_id in ids


def mark_processed(message_id):

    with open(PROCESSED_FILE, "a") as f:
        f.write(message_id + "\n")