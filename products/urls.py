from django.urls import path
from . views import product_list  , product_detail

urlpatterns = [
    path('', product_list ,name = 'product_list'),
    path('category/<int:subcategory_id>/',product_list ,name='product_by_category'),
    path('<slug:product_slug>', product_detail ,name = 'product_detail'),
]