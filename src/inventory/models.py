from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator

from users.models import CustomUser


class Material(models.Model):
    class Unit(models.TextChoices):
        LITRE = 'l', 'litre'
        KILOGRAM = 'kg', 'kilogram'
        M2 = 'm2', 'm²'
        PIECE = 'pcs', 'piece'
        PACK = 'pack', 'pack'
    name = models.CharField(max_length=64)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=10, choices=Unit.choices)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f'{self.name} - {self.quantity} {self.unit}, {self.unit_price} per one'
    

class Transaction(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=3, choices=[('IN', 'Incoming'), ('OUT', 'Outgoing')])
    date = models.DateField()
