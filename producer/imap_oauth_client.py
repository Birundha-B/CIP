import imaplib
from config.config import EMAIL, APP_PASSWORD
from producer.token_manager import get_access_token

_oauth_disabled = False
_logged_auth_mode = False


def connect_imap_oauth():
    global _oauth_disabled, _logged_auth_mode

    if not _oauth_disabled:
        try:
            access_token = get_access_token()
            if not access_token:
                raise ValueError("Access token is empty")
            auth_string = f"user={EMAIL}\x01auth=Bearer {access_token}\x01\x01"

            imap = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=15)
            imap.authenticate("XOAUTH2", lambda x: auth_string)

            if not _logged_auth_mode:
                print("IMAP OAuth connection successful")
                _logged_auth_mode = True
            return imap

        except Exception as oauth_err:
            _oauth_disabled = True
            if not _logged_auth_mode:
                print(f"OAuth unavailable ({type(oauth_err).__name__}), switching to App Password authentication...")

    if APP_PASSWORD:
        imap = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=15)
        imap.login(EMAIL, APP_PASSWORD)
        if not _logged_auth_mode:
            print("IMAP App Password connection successful")
            _logged_auth_mode = True
        return imap

    raise Exception("Both OAuth and App Password authentication failed.")