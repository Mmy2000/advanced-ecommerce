from .models import Settings , NewsLitter
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import translation


def my_settings(request):
    current_language = translation.get_language()
    about_site = Settings.objects.last()
    return {'about_site':about_site,'current_language':current_language}

def newsletter_footer(request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    NewsLitter.objects.create(email=email , name=name)
    return redirect('/')

