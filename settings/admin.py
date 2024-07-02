from django.contrib import admin
from .models import Contact , Settings , NewsLitter  , About , FAQ , Images
from parler.admin import TranslatableAdmin

# Register your models here.
admin.site.register(Contact)
admin.site.register(Settings,TranslatableAdmin)
admin.site.register(NewsLitter)
admin.site.register(About,TranslatableAdmin)
admin.site.register(Images,TranslatableAdmin)
admin.site.register(FAQ,TranslatableAdmin)
