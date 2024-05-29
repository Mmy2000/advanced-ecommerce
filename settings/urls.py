from django.urls import path
from . views import home , contact , newsletters , blog
from .api_view import about_api , api_post , api_post_category , filter_by_category_api , api_post_tags , filter_by_tag_api , api_newsletter,newsletter_subscription , contact_api , api_contact
from . settings_context import newsletter_footer

urlpatterns = [
    path('', home ,name = 'home'),
    path('contact/', contact ,name = 'contact'),
    path('blog/', blog ,name = 'blog'),
    path('newsletters/', newsletters ,name = 'newsletters'),
    path('newsletter_footer/', newsletter_footer ,name = 'newsletter_footer'),

    #api
    path('api/about' , about_api , name='about_api' ),
    path('api/posts' , api_post , name='api_post' ),
    path('api/newsletter' , api_newsletter , name='api_newsletter' ),
    path('api/newsletter/' , newsletter_subscription , name='newsletter_subscription' ),
    path('api/contact/', contact_api, name='contact_api'),
    path('api/contacts', api_contact, name='list_all_contacts'),
    path('api/posts/categories' , api_post_category , name='api_post_category' ),
    path('api/posts/categories/category=<str:query>' , filter_by_category_api , name='filter_by_category_api' ),
    path('api/posts/tags' , api_post_tags , name='api_post_tags' ),
    path('api/posts/tags/tag=<str:query>' , filter_by_tag_api , name='filter_by_tag_api' ),
]