from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models.query_utils import Q
from .models import Settings , NewsLitter , Post , Category , Contact
from .serializer import AboutSerializer , PostSerializer , CategorySerializer , TagsSerializer , NewsletterSerializer , ContactSerializer , TagListSerializerField
from taggit.models import Tag
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewsLitter
import json
import re
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def about_api(request):
    about = Settings.objects.last()
    data = AboutSerializer(about).data
    return Response({'data':data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_post(request):
    post = Post.objects.all()
    data = PostSerializer(post , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_post_category(request):
    category = Category.objects.all()
    data = CategorySerializer(category , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_by_category_api(request , query):
    post = Post.objects.filter(
        Q(category__name__icontains=query)
    )
    data = PostSerializer(post , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_post_tags(request):
    tag = Tag.objects.all()
    data = TagsSerializer(tag , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_by_tag_api(request , query):
    post = Post.objects.filter(
        Q(tags__name__icontains=query)
    )
    data = PostSerializer(post , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_newsletter(request):
    newsletter = NewsLitter.objects.all()
    data = NewsletterSerializer(newsletter , many=True , context={'request':request}).data
    return Response({'data':data})

@csrf_exempt
@permission_classes([IsAuthenticated])
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_contact(request):
    contact = Contact.objects.all()
    data = ContactSerializer(contact , many=True , context={'request':request}).data
    return Response({'data':data})

@csrf_exempt
@permission_classes([IsAuthenticated])
def contact_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            form = ContactForm(data)
            if form.is_valid():
                form.save()
                subject = "Welcome to EShopper site"
                message = "Our team will contact you within 24hrs."
                email_from = settings.EMAIL_HOST_USER
                email = form.cleaned_data['email']
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
                return JsonResponse({'message': 'Your message was sent successfully.'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid form submission', 'details': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)