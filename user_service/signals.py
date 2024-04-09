from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from news_service.models import NewsPost
from tengrinews.settings import EMAIL_HOST_USER


@receiver(post_save, sender=NewsPost)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = User.objects.filter(
            subscription__categories=instance.category, subscription__is_active=True
        ).distinct()

        for subscriber in subscribers:
            subject = "New news-post in Your Subscribed Category!!!"
            message = render_to_string(
                "html/email/notification_email.html", {"post": instance}
            )
            recipient_list = [subscriber.email]
            send_mail(
                subject, message, EMAIL_HOST_USER, recipient_list, html_message=message
            )
            print("SENDED")
