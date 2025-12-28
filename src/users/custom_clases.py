from django.contrib.auth.views import LoginView
from django.contrib import messages


class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        response.set_cookie(
            key='data',
            value='The quick brown fox jumps over the lazy dog',
            max_age=480,
            httponly=False,
            samesite="Lax"
        )
        messages.success(self.request, "Registration was successfull.")
        return response