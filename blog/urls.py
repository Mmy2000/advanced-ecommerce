from django.urls import path
from . views import  PostList , PostByCategory , PostByTags , PostDetail

urlpatterns = [
    path('', PostList.as_view() ,name = 'blog'),
    path('<int:pk>' , PostDetail.as_view() , name='post_detail'),
    path('category/<str:slug>' , PostByCategory.as_view() , name='post_by_category'),
    path('tags/<str:slug>' , PostByTags.as_view() , name='post_by_tags'),
]