from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config import settings

User = get_user_model()


@shared_task
def weekly_wish_email():
    users = User.objects.filter(is_active=True, email__isnull=False).exclude(email="")
    for user in users:
        try:
            send_mail(
                subject="Команда SkyLink бажає вам чудового тижня!",
                message="Нехай ваш тиждень буде легким, продуктивним і наповненим удачею 🚀",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f"An email has been sent to the user {user.email}")
        except Exception as e:
            print(f"Error sending to {user.email}: {e}")
