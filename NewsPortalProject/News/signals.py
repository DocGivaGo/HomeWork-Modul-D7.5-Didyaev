from django.db.models.signals import m2m_changed
from django.dispatch import receiver


from .models import *
from .tasks import send_notification


@receiver(m2m_changed, sender=PostCategory)
def task_about_new_post(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notification.delay(instance.preview(), instance.pk, instance.title, subscribers_emails)
