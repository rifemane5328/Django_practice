import logging
from captcha.fields import CaptchaField
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache

from utils.abc_analisys_helper import get_abc_statistics
from utils.transaction_helper import check_transaction
from .filters import MaterialFilter
from .forms import MaterialForm, TransactionForm
from .models import Material, Book, Basket, EmailLog

logger = logging.getLogger("cache")


# Materials
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

    paginate = request.GET.get('paginate') == 'on'

    if paginate:
        paginator = Paginator(materials_list, 2)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        elided_page_range = paginator.get_elided_page_range(
            number=page_obj.number, # current page
            on_each_side=3,
            on_ends=1
        )
    else:
        page_obj = materials_list
        elided_page_range = None
    return render(request, "inventory/get_materials.html",
                    {"materials": page_obj, "page_numbers": elided_page_range, "paginate": paginate})


def get_material_by_id(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, "inventory/material_by_id.html", {"material": material})


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


# Transactions
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


# Books
def get_books(request):
    cache_key = "books_list"
    books = cache.get(cache_key)
    if books is None:
        logger.warning("Дані з бази даних")
        books = list(Book.objects.all())
        cache.set(cache_key, books, timeout=300)
    else:
        logger.warning("Дані з cache")

    request.session['my_data'] = 'The quick brown fox jumps over the lazy dog' # records in session
    data = request.session.get('my_data', 'blank')
    return render(request, 'inventory/get_books.html', {"books": books, "data": data})


# Basket


@login_required
def basket_view(request):
    materials = Basket.objects.filter(user=request.user).select_related("material") # pulls up materials with one request
    return render(request, 'inventory/basket.html', {'materials': materials})


@login_required
def add_to_basket(request, material_id):
    material = Material.objects.get(id=material_id)
    current_user = request.user
    basket_item, created = Basket.objects.get_or_create(
        user=current_user,
        material=material,
        defaults={"count": 1}
    )
    if not created:
        basket_item.count +=1
        basket_item.save()

    return redirect('inventory:get_materials')


def delete_basket(request, material_id):
    Basket.objects.filter(user=request.user, material_id=material_id).delete()
    return redirect('inventory:basket_view')


def buy_material(request, material_id):
    basket = Basket.objects.filter(
        user=request.user,
        material_id=material_id
        )
    
    if not basket.exists():
        return redirect("inventory:basket_view")
    
    else: 
        basket.update(status="Bought")

        from_email = settings.EMAIL_HOST_USER
        material = basket.first().material
        unitary_basket = Basket.objects.get(user=request.user, material_id=material_id)

        message = (f'Ваша квитанція на оплату {material.name} на суму {material.unit_price * unitary_basket.count}.'
                    f'Просимо надіслати на пошту {from_email}.')
        to_email = request.user.email
        subject = "Квитанція на оплату"
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False
        )
        EmailLog.objects.create(to_email=to_email, subject=subject)


        messages.success(request, "Матеріал успішно придбано.")

    return redirect('inventory:basket_view')


@login_required
def basket_inc(request, material_id):
    basket = Basket.objects.get(user=request.user, material_id=material_id)
    count = basket.count + 1
    Basket.objects.filter(user=request.user, material_id=material_id).update(count=count)
    return redirect('inventory:basket_view')


@login_required
def basket_dec(request, material_id):
    basket = Basket.objects.get(user=request.user, material_id=material_id)
    count = basket.count - 1
    if count > 0:
        Basket.objects.filter(user=request.user, material_id=material_id).update(count=count)
    else:
        Basket.objects.filter(user=request.user, material_id=material_id).delete()
    return redirect('inventory:basket_view')

