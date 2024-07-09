from django.urls import path
from . views import product_list  , product_detail  , add_to_favourit ,  category_list , submit_review  ,deleteProduct, AddProduct,search

urlpatterns = [
    path('', product_list ,name = 'product_list'),
    path('category/<int:subcategory_id>/',product_list ,name='product_by_subcategory'),
    path('tag/<slug:tag_slug>/',product_list ,name='product_by_tag'),
    path('category/<int:subcategory_id>/<slug:product_slug>', product_detail ,name = 'product_detail'),
    path('categories/',category_list ,name='categories'),
    path('add_to_favourit/<int:id>',add_to_favourit ,name='add_to_favourit'),
    path('submit_review/<int:product_id>/',submit_review ,name='submit_review'),
    path( 'new/',AddProduct.as_view() , name='product_new' ),
    path( 'delete/<int:id>',deleteProduct , name='deleteProduct' ),
    path('search/',search ,name='search'),
]