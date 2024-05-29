from django.urls import path
from . import views
from . import api_view
urlpatterns = [
    path('', views.cart , name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart , name='add_cart'),
    path('apply_coupon/', views.apply_coupon , name='apply_coupon'),
    path('checkout/', views.checkout , name='checkout'),
    path('decrement_cart/<int:product_id>/<int:cart_item_id>/', views.decrement_cart , name='decrement_cart'),
    path('delete_cart/<int:product_id>/<int:cart_item_id>/', views.delete_cart , name='delete_cart'),

    #api
    path('api/cart/', api_view.CartAPIView.as_view(), name='cart_api'),
    path('api/add_to_cart/<int:product_id>/', api_view.AddToCart.as_view(), name='add_to_cart'),
    path('api/decrement_cart/<int:product_id>/<int:cart_item_id>/', api_view.DecrementCart.as_view(), name='decrement_cart'),
    path('api/delete_cart/<int:product_id>/<int:cart_item_id>/', api_view.DeleteCartItem.as_view(), name='delete_cart'),
    path('api/checkout/', api_view.CheckoutAPIView.as_view(), name='cart_api'),


]
