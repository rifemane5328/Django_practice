from django.urls import path
from inventory.views import add_material_view, get_all_materials, get_material_details


app_name = 'inventory'


urlpatterns = [
    path('add-material/', add_material_view, name='add_material'),
    path('get-all-materials', get_all_materials, name='get_materials'),
    path('get-material/<int:material_id>/', get_material_details, name='material_details'),
]
