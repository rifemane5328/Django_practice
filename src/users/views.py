from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm, CustomUserForm
from .models import CustomUser


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, message='Registration was successfull.')
            response = redirect('inventory:get_materials')

            response.set_cookie(
                key="data",
                value="The quick brown fox jumps over the lazy dog",
                max_age=480,
                httponly=False,
                samesite="Lax",
                secure=True
            )
            return response
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = RegistrationForm()
        
    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, message='Profile has been updated successfully.')
        else:
            messages.error(request, message='Something went wrong.')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, "users/profile.html", {"form": form})


def google_login(request):
    fastapi_login_url = 'http://127.0.0.1:8001/login/google'
    return redirect(fastapi_login_url)


def login_from_fastapi(request):
    email = request.GET.get("email")
    name = request.GET.get("name")
    sub = request.GET.get("sub")
    if not email:
        return redirect("auth:login")
    user, created = CustomUser.objects.get_or_create(
        email=email,
        default={
            "name": name,
            "password": "123",
            "is_active": True
        }
    )

    messages.success(request, f"Ви ввійшли як {user.name}")

    login(request, user)
    
    response = redirect("inventory:get_materials")
    response.set_cookie(
        key="data",
        value="The quick brown fox jumps over the lazy dog",
        max_age=480,
        httponly=False,
        samesite="Lax",
        secure=True
    )
    return response