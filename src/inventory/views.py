from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, F

from utils.abc_analisys_helper import get_abc_statistics
from utils.transaction_helper import check_transaction
from .filters import MaterialFilter
from .forms import MaterialForm, TransactionForm
from .models import Material

@login_required
def add_material_view(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
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


@login_required
def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(data=request.POST, request=request)
        if form.is_valid():
            try:
                check_transaction(
                    form.cleaned_data["material"],
                    form.cleaned_data["quantity"],
                    form.cleaned_data["transaction_type"]
                )
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, "Transaction has been created")
                return redirect("inventory:get_materials")
            except ValidationError as e:
                form.add_error(None, list(e))
    else:
        form = TransactionForm(request=request)
    return render(request, 'inventory/add_transaction.html', {"form": form})


@login_required
def material_abc_view(request):
    queryset = Material.objects.filter(
        user=request.user, transaction__transaction_type='OUT'
    ).annotate(
        total_amount_pu=Sum('transaction__quantity'), # pu means per unit, that is per one material
        total_expenses_pu=Sum('transaction__quantity') * F('unit_price')
    ).values(
        'id', 'name', 'unit', 'total_amount_pu', 'total_expenses_pu'
    ).order_by('-total_expenses_pu')
    calculated_data = get_abc_statistics(queryset)
    return render(request, 'inventory/materials_abc_stats.html',
                    {"pd_data": calculated_data.to_dict(orient='records')})