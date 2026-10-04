from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from common.encryption import decrypt_message
from config.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    TOKEN_URI,
    ENCRYPTED_REFRESH_TOKEN
)

SCOPES = ['https://mail.google.com/']


def get_access_token():

    refresh_token = decrypt_message(
        ENCRYPTED_REFRESH_TOKEN.encode()
    )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES
    )

    creds.refresh(Request())

    return creds.token