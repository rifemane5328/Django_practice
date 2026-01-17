from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

from users.models import CustomUser

current_year = date.today().year

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


class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    year = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(current_year)])
    number_of_pages = models.IntegerField()
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'{self.title} - {self.author}, issued in {self.year}, has {self.number_of_pages} pages and rating {self.rating}'
    

class Basket(models.Model):
    class StatusBin(models.TextChoices):
        Added = 'A', 'Added' # when material just added to basket
        Bought = 'B', 'Bought'# when user confirmed an intention to buy material
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    status = models.CharField(choices=StatusBin.choices, default=StatusBin.Added)
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ("user", "material")


class SystemLog(models.Model):
    LEVELS = (
        ("INFO", "INFO"),
        ("WARNING", "WARNING"),
        ("ERROR", "ERROR")
    )
    
    level = models.CharField(max_length=10, choices=LEVELS)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.level}] {self.created_at:%Y-%m-%d %H:%M}"
    

class EmailLog(models.Model):
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
