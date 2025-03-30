from django.conf import settings
from django.core.mail import EmailMessage


def send_ticket_email(email: str, path_file: str) -> None:
    email = EmailMessage(
        subject="Airport Ticket",
        body="Ваш билет во вложении.",
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    email.attach_file(f"{path_file}")
    email.send()
