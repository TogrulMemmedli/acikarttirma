
import os

import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

if not RESEND_API_KEY:
    raise RuntimeError("RESEND_API_KEY .env faylında təyin edilməyib.")

if not EMAIL_FROM:
    raise RuntimeError("EMAIL_FROM .env faylında təyin edilməyib.")

resend.api_key = RESEND_API_KEY


def send_email(to: str, subject: str, html: str):
    params = {
        "from": EMAIL_FROM,
        "to": [to],
        "subject": subject,
        "html": html,
    }

    return resend.Emails.send(params)
