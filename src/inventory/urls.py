from django.urls import path
from inventory.views import (add_material_view, get_all_materials, get_material_by_id,
                            create_transaction, material_abc_view)


app_name = 'inventory'


urlpatterns = [
    path('add-material/', add_material_view, name='add_material'),
    path('get-all-materials/', get_all_materials, name='get_materials'),
    path('get-material/<int:material_id>/', get_material_by_id, name='get_material_by_id'),
    path("create-transaction/", create_transaction, name="create_transaction"),
    path('material-abc-stats/', material_abc_view, name='material_abc_stats')
]
