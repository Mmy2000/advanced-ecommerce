from .models import Settings , NewsLitter
from django.http import JsonResponse


def my_settings(request):
    about_site = Settings.objects.last()
    return {'about_site':about_site}

def newsletter_footer(request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    NewsLitter.objects.create(email=email , name=name)
    return JsonResponse({'done':'done'})