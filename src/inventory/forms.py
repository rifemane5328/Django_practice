from django import forms
from .models import Material, Transaction

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit_price', 'unit', 'quantity', 'user']
        labels = {
            "name": ("Material"),
        }
        help_texts = {
            "name": ("The title of material"),
            "quantity": ("Total quantity of units"),
            "unit_price": ("Price per unit of product")
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["material", "quantity", "transaction_type", "date"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields["material"].queryset = Material.objects.filter(
                user = self.request.user
            )
