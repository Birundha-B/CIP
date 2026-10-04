
from cryptography.fernet import Fernet

from config.config import FERNET_KEY


# ==================================================
# FERNET CONFIGURATION
# ==================================================

if not FERNET_KEY:
    raise Exception(
        "FERNET_KEY not set in the project .env file"
    )

cipher = Fernet(
    FERNET_KEY.encode()
)


# ==================================================
# ENCRYPT MESSAGE
# ==================================================

def encrypt_message(message: str) -> bytes:
    return cipher.encrypt(
        message.encode()
    )


# ==================================================
# DECRYPT MESSAGE
# ==================================================

def decrypt_message(token: bytes) -> str:
    return cipher.decrypt(
        token
    ).decode()

