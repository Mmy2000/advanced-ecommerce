from django.contrib import admin
from .models import Contact , Settings , NewsLitter  , About , FAQ
# Register your models here.
admin.site.register(Contact)
admin.site.register(Settings)
admin.site.register(NewsLitter)
admin.site.register(About)
admin.site.register(FAQ)
