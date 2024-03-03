from django.urls import path
from . views import home , contact , newsletters

urlpatterns = [
    path('', home ,name = 'home'),
    path('contact/', contact ,name = 'contact'),
    path('newsletters/', newsletters ,name = 'newsletters'),
]