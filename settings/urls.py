from django.urls import path
from . views import home , contact , newsletters 
from . settings_context import newsletter_footer

urlpatterns = [
    path('', home ,name = 'home'),
    path('contact/', contact ,name = 'contact'),
    path('newsletters/', newsletters ,name = 'newsletters'),
    path('newsletter_footer/', newsletter_footer ,name = 'newsletter_footer'),
]