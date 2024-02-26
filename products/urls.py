from django.urls import path
from . views import product_list  , product_detail , search , add_to_favourit

urlpatterns = [
    path('', product_list ,name = 'product_list'),
    path('category/<int:subcategory_id>/',product_list ,name='product_by_subcategory'),
    path('brands/<slug:brand_slug>/',product_list ,name='product_by_brand'),
    path('tag/<slug:tag_slug>/',product_list ,name='product_by_tag'),
    path('<slug:product_slug>', product_detail ,name = 'product_detail'),
    path('search/',search ,name='search'),
    path('add_to_favourit/<int:id>',add_to_favourit ,name='add_to_favourit'),

]