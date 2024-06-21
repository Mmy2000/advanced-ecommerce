from django.urls import path
from . views import product_list  , product_detail , search , add_to_favourit , filter_by_price , filter_by_variations , category_list , submit_review , search_result ,  load_subcategories
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
    path('load-subcategories/', load_subcategories, name='load_subcategories'),

    #api
    path('api/list' , api_view.product_list, name='products_api_list'),
    path('api/list/variation' , api_view.variations, name='variation'),
    path('api/list/<int:id>' , api_view.product_deatils_api, name='products_api_detail'),
    path('api/subcategories' , api_view.subcategory_api, name='subcategory_api'),
    path('api/categories' , api_view.category_api, name='category_api'),
    path('api/categories/category=<str:query>' , api_view.searchByCategory, name='searchByCategory'),
    path('api/subcategory/subcategory=<str:query>' , api_view.searchBySubcategory, name='searchBySubcategory'),
    path('api/category/query=<str:query>' , api_view.getAllSubcategoriesInCategories, name='getAllSubcategoriesInCategories'),
    path('api/brands/brand=<str:query>' , api_view.searchByBrand, name='searchByBrand'),
    path('api/brands' , api_view.brand_api, name='brand_api'),
    path('api/tags' , api_view.tags_api, name='tags_api'),
    path('api/tags/tag=<str:query>' , api_view.searchByTag, name='searchByTag'),
    path('api/search/query=<str:query>' , api_view.search_api, name='search_api'),
    path('api/list/ordered_by_createdAt' , api_view.product_list_ordered_by_createdAt_api, name='products_api_list_ordered_by_createdAt'),
    path('api/list/ordered_by_papularty' , api_view.product_list_ordered_by_papularty_api, name='products_api_list_ordered_by_papularty'),
    path('api/list/ordered_by_review' , api_view.product_list_ordered_by_review_api, name='products_api_list_ordered_by_review'),
    path('api/list/ordered_by_price_low_to_high' , api_view.product_list_ordered_by_price_api, name='products_api_list_ordered_by_price'),
    path('api/list/ordered_by_price_high_to_low' , api_view.product_list_ordered_by_price2_api, name='products_api_list_ordered_by_price2'),
    path('api/list/variation/' , api_view.product_list_api_filter, name='product_list_api_filter'),
    path('api/list/price/' , api_view.filter_by_price_api, name='filter_by_price_api'),
    path('api/favourite/<int:id>/', api_view.AddToFavouriteAPIView.as_view(), name='add_to_favourite'),
    path('api/submit_review/<product_id>/', api_view.SubmitReview.as_view(), name='submit_review'),
]