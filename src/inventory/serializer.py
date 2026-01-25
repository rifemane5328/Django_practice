from rest_framework import serializers

from .models import Material, Basket


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ["id", "name", "unit_price", "unit", "quantity", "user"]


class BasketSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(slug_field="name", read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)
    
    class Meta:
        model = Basket
        fields = ["id", "user", "material", "status", "count"]