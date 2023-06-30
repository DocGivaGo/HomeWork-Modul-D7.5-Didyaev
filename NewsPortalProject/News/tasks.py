import datetime

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from .models import *


@shared_task
def send_notification(preview, pk, title,
                      subscribers):  # отдельно делаем функцию отправки сообщения о новом посте для подписчика
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/post/{pk}'  # http://127.0.0.1:8000/post/pk
        }
    )
    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def email_every_monday():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    adver = Post.objects.filter(dateCreation__gte=last_week)
    users = set(User.objects.all().values_list('email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'adver': adver,
        }
    )
    for email in users:
        send_mail(
            subject='Публикации за неделю',
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_content,
        )
