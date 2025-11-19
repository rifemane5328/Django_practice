from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm, CustomUserForm


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("inventory:get_materials")
    form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, message='Profile has been created successfully.')
        else:
            messages.error(request, message='Something went wrong.')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, "users/profile.html", {"form": form})