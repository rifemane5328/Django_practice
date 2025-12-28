from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Material


@receiver(post_save, sender=Material)
def material_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"Новий матеріал створено: {instance.name} від {instance.user}")