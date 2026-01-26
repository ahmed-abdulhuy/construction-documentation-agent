import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import emails  # type: ignore
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError

from app.core.env_settings import ENV_VARS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert ENV_VARS.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(ENV_VARS.EMAILS_FROM_NAME, ENV_VARS.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": ENV_VARS.SMTP_HOST, "port": ENV_VARS.SMTP_PORT}
    if ENV_VARS.SMTP_TLS:
        smtp_options["tls"] = True
    elif ENV_VARS.SMTP_SSL:
        smtp_options["ssl"] = True
    if ENV_VARS.SMTP_USER:
        smtp_options["user"] = ENV_VARS.SMTP_USER
    if ENV_VARS.SMTP_PASSWORD:
        smtp_options["password"] = ENV_VARS.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    project_name = ENV_VARS.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": ENV_VARS.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = ENV_VARS.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{ENV_VARS.FRONTEND_HOST}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": ENV_VARS.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": ENV_VARS.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = ENV_VARS.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": ENV_VARS.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": ENV_VARS.FRONTEND_HOST,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=ENV_VARS.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        ENV_VARS.SECRET_KEY,
        algorithm=ENV_VARS.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, ENV_VARS.SECRET_KEY, algorithms=[ENV_VARS.ALGORITHM]
        )
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None