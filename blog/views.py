from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Post , Category
from taggit.models import Tag
from django.db.models import Count
from django.db.models.query_utils import Q


# Create your views here.
class PostList(ListView):
    model = Post
    paginate_by = 6
    def get_queryset(self) :
        name = self.request.GET.get('q','')
        language = self.request.LANGUAGE_CODE
        object_list = Post.objects.language(language).filter(
            Q(translations__title__icontains = name) |
            Q(translations__description__icontains=name)
        ).distinct() 
        return object_list

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().annotate(post_count=Count('post_category'))
        context["tags"] = Tag.objects.filter(post__isnull=False).distinct()
        context["recent_posts"] = Post.objects.all()[:3]
        return context
    def get(self, request, *args, **kwargs):
        # Get the post object
        self.object = self.get_object()
        # Increase the view count
        self.object.views += 1
        self.object.save()
        # Call the superclass implementation of get to handle the rest
        return super().get(request, *args, **kwargs)
    
class PostByCategory(ListView):
    model = Post

    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Post.objects.filter(
            Q(category__name__icontains = slug)
        )
        return object_list
    
class PostByTags(ListView):
    model = Post

    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Post.objects.filter(
            Q(tags__name__icontains = slug)
        )
        return object_list