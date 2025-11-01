from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator


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


    def __str__(self):
        return self.name
