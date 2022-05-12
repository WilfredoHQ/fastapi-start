from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import emails
from emails.template import JinjaTemplate
from jose import jwt

from app.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: dict[str, Any] = {},
) -> None:
    if settings.EMAILS_ENABLED:
        message = emails.Message(
            subject=JinjaTemplate(subject_template),
            html=JinjaTemplate(html_template),
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )
        smtp_options = {
            "tls": settings.SMTP_TLS,
            "port": settings.SMTP_PORT,
            "host": settings.SMTP_HOST,
            "user": settings.SMTP_USER,
            "password": settings.SMTP_PASSWORD,
        }
        message.send(to=email_to, render=environment, smtp=smtp_options)


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - ¿Olvidaste tu contraseña?"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset.html", encoding="utf-8") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "valid_minutes": settings.EMAIL_RESET_TOKEN_EXPIRE_MINUTES,
            "link": f"{settings.CLIENT_HOST}/restablecer?token={token}",
        },
    )


def send_welcome_email(email_to: str, full_name: str | None) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - ¡Bienvenido {full_name}!"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "welcome.html", encoding="utf-8"
    ) as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "full_name": full_name,
            "project_name": project_name,
            "link": settings.CLIENT_HOST,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(minutes=settings.EMAIL_RESET_TOKEN_EXPIRE_MINUTES)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None
