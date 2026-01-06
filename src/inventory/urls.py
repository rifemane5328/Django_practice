from django.urls import path
from inventory.views import (add_material_view, get_all_materials, get_material_by_id,
                            create_transaction, material_abc_view, get_books, create_basket,
                            basket_view, delete_basket, buy_material, basket_inc, basket_dec)


app_name = 'inventory'


urlpatterns = [
    path('add-material/', add_material_view, name='add_material'),
    path('get-all-materials/', get_all_materials, name='get_materials'),
    path('get-material/<int:material_id>/', get_material_by_id, name='get_material_by_id'),
    path("create-transaction/", create_transaction, name='create_transaction'),
    path('material-abc-stats/', material_abc_view, name='material_abc_stats'),
    path('get-books/', get_books, name='get_books'),
    path('get-all-materials/add-basket/<int:material_id>/', create_basket, name='add_basket'),
    path('basket-view', basket_view, name='basket_view'),
    path('delete-basket/<int:material_id>/', delete_basket, name='delete_basket'), # deletes material from basket
    path('buy-material/<int:material_id>/', buy_material, name='buy_material'), 
    path('inc/<int:material_id>/', basket_inc, name='inc_material'),
    path('dec/<int:material_id>/', basket_dec, name='dec_material')
]
