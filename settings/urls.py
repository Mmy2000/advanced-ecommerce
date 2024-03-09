from django.urls import path
from . views import home , contact , newsletters , blog
from . settings_context import newsletter_footer

urlpatterns = [
    path('', home ,name = 'home'),
    path('contact/', contact ,name = 'contact'),
    path('blog/', blog ,name = 'blog'),
    path('newsletters/', newsletters ,name = 'newsletters'),
    path('newsletter_footer/', newsletter_footer ,name = 'newsletter_footer'),
]