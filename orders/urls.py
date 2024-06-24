from django.urls import path
from . import views
urlpatterns = [
    path('place_order/', views.place_order , name='place_order'),
    path('payments/', views.payments , name='payments'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
]
