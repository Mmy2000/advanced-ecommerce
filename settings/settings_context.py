from .models import Settings


def my_settings(request):
    about_site = Settings.objects.last()
    return {'about_site':about_site}