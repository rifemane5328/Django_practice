from django.db import transaction
from inventory.models import Material
from django.core.exceptions import ValidationError


def check_transaction(material, quantity, transaction_type):
    with transaction.atomic():
        material = Material.objects.select_for_update().get(id=material.id)
        # if quantity of material is lower than that which should be substracted
        if transaction_type == "OUT" and material.quantity < quantity:
            raise ValidationError("Insufficient quantity of material")
        material.quantity += quantity if transaction_type == "IN" else -quantity
        material.save()