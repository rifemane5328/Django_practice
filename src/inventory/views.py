from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .filters import MaterialFilter
from .forms import MaterialForm
from .models import Material

@login_required
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
    my_filter = MaterialFilter(request.GET, queryset=materials)
    materials_list = my_filter.qs

    paginator = Paginator(materials_list, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    elided_page_range = paginator.get_elided_page_range(
        number=page_obj.number, # current page
        on_each_side=3,
        on_ends=1
    )

    return render(request, "inventory/get_materials.html",
                    {"materials": page_obj, "page_numbers": elided_page_range})


def get_material_by_id(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, "inventory/material_by_id.html", {"material": material})
