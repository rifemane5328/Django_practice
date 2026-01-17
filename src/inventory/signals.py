from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from .models import Basket, Book, EmailLog


@receiver(post_save, sender=Book)
def invalidate_books_cache(sender, **kwargs):
    cache.delete("books_list")


@receiver(post_save, sender=Basket)
def material_created_signal(sender, instance, created, **kwargs):
    if created:
        from_email = settings.EMAIL_HOST_USER
        message = f'Ви додали курс {instance.material.name} в корзину'
        to_email = instance.user.email
        send_mail(
            "Курс додано в корзину",
            message,
            from_email,
            [to_email],
            fail_silently=False,
        )
        EmailLog.objects.create(
            subject="Курс додано в корзину",
            to_email=to_email,
        )