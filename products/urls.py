from django.urls import path
from . views import product_list  , product_detail , search , add_to_favourit , filter_by_price , filter_by_variations , category_list , submit_review , product_list_orderd_by_rating , product_list_orderd_by_papularty , product_list_orderd_by_price , product_list_orderd_by_created , product_list_orderd_by_price2 , search_result
from . import api_view
urlpatterns = [
    path('', product_list ,name = 'product_list'),
    path('category/<int:subcategory_id>/',product_list ,name='product_by_subcategory'),
    path('brands/<slug:brand_slug>/',product_list ,name='product_by_brand'),
    path('tag/<slug:tag_slug>/',product_list ,name='product_by_tag'),
    path('category/<int:subcategory_id>/<slug:product_slug>', product_detail ,name = 'product_detail'),
    path('search/',search ,name='search'),
    path('results/',search_result ,name='results'),
    path('categories/',category_list ,name='categories'),
    path('add_to_favourit/<int:id>',add_to_favourit ,name='add_to_favourit'),
    path('filter_by_price/',filter_by_price ,name='filter_by_price'),
    path('filter_by_variations/',filter_by_variations ,name='filter_by_variations'),
    path('submit_review/<int:product_id>/',submit_review ,name='submit_review'),
    path('orderd_by_rating/',product_list_orderd_by_rating,name='product_list_orderd_by_rating'),
    path('orderd_by_created/',product_list_orderd_by_created , name='product_list_orderd_by_created'),
    path('orderd_by_popularty/',product_list_orderd_by_papularty , name='product_list_orderd_by_papularty'),
    path('orderd_by_price/',product_list_orderd_by_price , name='product_list_orderd_by_price'),
    path('orderd_by_highest price/',product_list_orderd_by_price2 , name='product_list_orderd_by_price2'),
    #api
    path('api/list' , api_view.product_list, name='products_api_list'),
    path('api/list/<int:id>' , api_view.product_deatils_api, name='products_api_detail'),
    path('api/subcategories' , api_view.subcategory_api, name='subcategory_api'),
    path('api/categories' , api_view.category_api, name='category_api'),
    path('api/categories/<str:query>' , api_view.searchByCategory, name='searchByCategory'),
    path('api/brands' , api_view.brand_api, name='brand_api'),
    path('api/tags' , api_view.tags_api, name='tags_api'),
    path('api/search/<str:query>' , api_view.search_api, name='search_api'),
]