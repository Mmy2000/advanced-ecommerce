from django.urls import path
from . views import product_list  , product_detail , search 

urlpatterns = [
    path('', product_list ,name = 'product_list'),
    path('category/<int:subcategory_id>/',product_list ,name='product_by_subcategory'),
    path('brands/<slug:brand_slug>/',product_list ,name='product_by_brand'),
    path('<slug:product_slug>', product_detail ,name = 'product_detail'),
    path('search/',search ,name='search'),

]