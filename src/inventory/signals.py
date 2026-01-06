from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from .models import Material, Book


@receiver(post_save, sender=Book)
def invalidate_books_cache(sender, **kwargs):
    cache.delete("books_list")


@receiver(post_save, sender=Material)
def material_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"Новий матеріал створено: {instance.name} від {instance.user}")