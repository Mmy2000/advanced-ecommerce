from rest_framework.response import Response
from rest_framework.decorators import api_view 
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models.query_utils import Q
from .models import Settings , NewsLitter , Post , Category
from .serializer import AboutSerializer , PostSerializer , CategorySerializer , TagsSerializer , NewsletterSerializer
from taggit.models import Tag
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewsLitter
import json
import re

@api_view(['GET'])
def about_api(request):
    about = Settings.objects.last()
    data = AboutSerializer(about).data
    return Response({'data':data})

@api_view(['GET'])
def api_post(request):
    post = Post.objects.all()
    data = PostSerializer(post , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def api_post_category(request):
    category = Category.objects.all()
    data = CategorySerializer(category , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def filter_by_category_api(request , query):
    post = Post.objects.filter(
        Q(category__name__icontains=query)
    )
    data = PostSerializer(post , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def api_post_tags(request):
    tag = Tag.objects.all()
    data = TagsSerializer(tag , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def filter_by_tag_api(request , query):
    post = Post.objects.filter(
        Q(tags__name__icontains=query)
    )
    data = PostSerializer(post , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def api_newsletter(request):
    newsletter = NewsLitter.objects.all()
    data = NewsletterSerializer(newsletter , many=True , context={'request':request}).data
    return Response({'data':data})

@csrf_exempt
def newsletter_subscription(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            name = data.get('name')

            # Basic email validation
            if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return JsonResponse({'error': 'Invalid email format'}, status=400)

            # Save to the database
            NewsLitter.objects.create(email=email , name=name)
            return JsonResponse({'done': 'done'}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


