from django.contrib import admin
from .models import Contact , Settings , NewsLitter  , About , FAQ , Images
# Register your models here.
admin.site.register(Contact)
admin.site.register(Settings)
admin.site.register(NewsLitter)
admin.site.register(About)
admin.site.register(Images)
admin.site.register(FAQ)
