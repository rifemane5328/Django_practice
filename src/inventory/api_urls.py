from django.urls import path
from .api_views import MaterialListAPI, MaterialCreateAPI, BasketListAPI, GoogleLoginView, GoogleCallbackView


urlpatterns = [
    path("materials/", MaterialListAPI.as_view(), name="api_materials"),
    path("materials/create/", MaterialCreateAPI.as_view(), name="api_materials_create"),
    path("baskets/", BasketListAPI.as_view(), name="api_baskets"),
    path("auth/google/login/", GoogleLoginView.as_view()),
    path("auth/google/callback/", GoogleCallbackView.as_view())
]