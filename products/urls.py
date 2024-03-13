from django.urls import path
from . views import product_list  , product_detail , search , add_to_favourit , filter_by_price , filter_by_variations , category_list , submit_review

urlpatterns = [
    path('', product_list ,name = 'product_list'),
    path('category/<int:subcategory_id>/',product_list ,name='product_by_subcategory'),
    path('brands/<slug:brand_slug>/',product_list ,name='product_by_brand'),
    path('tag/<slug:tag_slug>/',product_list ,name='product_by_tag'),
    path('category/<int:subcategory_id>/<slug:product_slug>', product_detail ,name = 'product_detail'),
    path('search/',search ,name='search'),
    path('categories/',category_list ,name='categories'),
    path('add_to_favourit/<int:id>',add_to_favourit ,name='add_to_favourit'),
    path('filter_by_price/',filter_by_price ,name='filter_by_price'),
    path('filter_by_variations/',filter_by_variations ,name='filter_by_variations'),
    path('submit_review/<int:product_id>/',submit_review ,name='submit_review'),
]