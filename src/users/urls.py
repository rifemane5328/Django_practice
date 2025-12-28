from django.urls import path, reverse_lazy
from .custom_clases import CustomLoginView
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordChangeView

from .views import register_view, profile_view, google_login, login_from_fastapi


app_name = 'auth'

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile_view"),
    path("login/google/", google_login, name="google_login"),
    path("login/from-fastapi/", login_from_fastapi, name="login_from_fastapi"),
    path("password/change/", PasswordChangeView.as_view(
        template_name="users/password_change.html",
        success_url=reverse_lazy("auth:password_change_done")),
        name="password_change"
        ),
    path("password/change/done/", PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html"), name="password_change_done")
]