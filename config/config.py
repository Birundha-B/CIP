
from pathlib import Path
import os
from dotenv import load_dotenv


# ==================================================
# ENVIRONMENT CONFIGURATION
# ==================================================

# Project root:
# C:\Users\prane\Downloads\CIP_SEM6
BASE_DIR = Path(__file__).resolve().parent.parent

# Explicitly use the .env in the project root
ENV_FILE = BASE_DIR / ".env"

# Load this exact .env file
load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


# ==================================================
# EMAIL CONFIG
# ==================================================

EMAIL = os.getenv("EMAIL")

SMTP_SERVER = os.getenv(
    "SMTP_SERVER",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.getenv("SMTP_PORT", "465")
)

APP_PASSWORD = os.getenv("APP_PASSWORD")


# ==================================================
# RABBITMQ CONFIG
# ==================================================

RABBITMQ_HOST = os.getenv(
    "RABBITMQ_HOST",
    "localhost"
)

RABBITMQ_PORT = int(
    os.getenv("RABBITMQ_PORT", "5672")
)

RABBITMQ_QUEUE = os.getenv(
    "RABBITMQ_QUEUE",
    "email_queue"
)

RABBITMQ_EXCHANGE = os.getenv(
    "RABBITMQ_EXCHANGE",
    "email_exchange"
)

DLQ_EXCHANGE = os.getenv(
    "DLQ_EXCHANGE",
    "dlx_exchange"
)

DLQ_QUEUE = os.getenv(
    "DLQ_QUEUE",
    "email_dlq"
)


# ==================================================
# ENCRYPTION CONFIG
# ==================================================

FERNET_KEY = os.getenv("FERNET_KEY")


# ==================================================
# OAUTH CONFIG (GMAIL IMAP)
# ==================================================

CLIENT_ID = os.getenv("CLIENT_ID")

CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN_URI = os.getenv("TOKEN_URI")

ENCRYPTED_REFRESH_TOKEN = os.getenv(
    "ENCRYPTED_REFRESH_TOKEN"
)


# ==================================================
# ML / DECISION ENGINE CONFIG
# ==================================================

CONFIDENCE_THRESHOLD = float(
    os.getenv(
        "CONFIDENCE_THRESHOLD",
        "0.75"
    )
)


# ==================================================
# DEPARTMENT EMAIL ROUTING
# ==================================================

DEPARTMENT_EMAILS = {
    # Original 6
    "hr":                          "cipprojecthr@gmail.com",
    "it support":                  "cipprojectitsupport@gmail.com",
    "accounts":                    "cipprojectfinance@gmail.com",
    "security":                    "cipprojectcomplaint@gmail.com",
    "administration":              "cipprojectads@gmail.com",
    "network":                     "cipprojectmanual@gmail.com",
    # New 6
    "facilities & maintenance":    "cipprojecthr@gmail.com",
    "quality assurance":           "cipprojectitsupport@gmail.com",
    "data / analytics":            "cipprojectfinance@gmail.com",
    "engineering":                 "cipprojectcomplaint@gmail.com",
    "product development":         "cipprojectads@gmail.com",
    "research & development":      "cipprojectmanual@gmail.com",
}


# ==================================================
# FALLBACK / MANUAL REVIEW
# ==================================================

MANUAL_REVIEW_EMAIL = os.getenv(
    "MANUAL_REVIEW_EMAIL",
    "cipprojectmanual@gmail.com"
)


# ==================================================
# LOGGING CONFIG
# ==================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)


# ==================================================
# RETRY CONFIG
# ==================================================

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "3")
)

RETRY_DELAY = int(
    os.getenv("RETRY_DELAY", "5")
)

