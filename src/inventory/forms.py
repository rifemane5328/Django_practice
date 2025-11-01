from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit_price', 'unit', 'quantity']
        labels = {
            "name": ("Material"),
        }
        help_texts = {
            "name": ("The title of material"),
            "quantity": ("Total quantity of units"),
            "unit_price": ("Price per unit of product")
        }
