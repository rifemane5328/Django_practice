from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import MaterialForm
from .models import Material

def add_material_view(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.save()
            messages.success(request, "Material has been created")
            return redirect("inventory:add_material") 
    form = MaterialForm()
    return render(request, "inventory/add_material.html", {"form": form})


def get_all_materials(request):
    materials = Material.objects.all()
    return render(request, "inventory/get_materials.html", {"materials": materials})


def get_material_details(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, "inventory/material_details.html", {"material": material})
