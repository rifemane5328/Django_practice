from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from ninja.security import django_auth
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Material, Basket
from .serializer import MaterialSerializer, BasketSerializer
from stocks.secret import oauth
from users.models import CustomUser
from .schemas import MaterialOut, MaterialIn, ChangeMaterial

api_ninja = NinjaAPI()

# Material
class MaterialListAPI(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialCreateAPI(generics.CreateAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Basket
class BasketListAPI(generics.ListAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer


class GoogleLoginView(APIView):
    def get(self, request):
        redirect_uri = 'http://localhost:8000/api/auth/google/callback/'
        return oauth.google.authorize_redirect(request, redirect_uri)
    

class GoogleCallbackView(APIView):
    def get(self, request):
        token = oauth.google.authorize_access_token(request)
        response = oauth.google.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            token=token
            )
        user_info = response.json()

        email = user_info['email']
        name = user_info.get('name', '')
        sub = user_info.get('sub') # for the identification

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': name
            }
        )

        login(request, user)
        response = redirect('inventory:get_materials')

        response.set_cookie(
        key="data",
        value="The quick brown fox jumps over the lazy dog",
        max_age=480,
        httponly=False,
        samesite="Lax",
        secure=True)

        return response
    

@api_ninja.get("/get-materials", response=list[MaterialOut])
def get_materials(request):
    return Material.objects.all()


@api_ninja.get("/get-materials/{material_id}", response=MaterialOut)
def get_material_by_id(request, material_id: int):
    return get_object_or_404(Material, id=material_id)


@api_ninja.post("/create-material", response=MaterialOut)
@csrf_exempt
def create_material(request, data: MaterialIn):
    material = Material.objects.create(
        name=data.name,
        unit_price=data.unit_price,
        unit=data.unit,
        quantity=data.quantity,
        user=request.user
    )

    return material


@api_ninja.patch("/change-material/{material_id}", response=MaterialOut)
@csrf_exempt
def change_material(request, material_id: int, data: ChangeMaterial):
    material = get_object_or_404(Material, id=material_id)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(material, key, value)

    material.save()
    return material


@api_ninja.put("/replace-material/{material_id}", response=MaterialOut)
@csrf_exempt
def replace_material(request, material_id: int, data: MaterialIn):
    material = get_object_or_404(Material, id=material_id)

    for key, value in data.dict().items():
        setattr(material, key, value) # sets every material's field(key) to value

    material.save()
    return material


@api_ninja.delete("/delete-material/{material_id}")
@csrf_exempt
def delete_material(request, material_id: int):
    material = get_object_or_404(Material, id=material_id)
    material.delete()
    return {"success": "True"}

