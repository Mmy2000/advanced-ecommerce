from django.contrib import admin
from .models import Contact , Settings , NewsLitter , Post , Category
# Register your models here.
admin.site.register(Contact)
admin.site.register(Settings)
admin.site.register(NewsLitter)
admin.site.register(Post)
admin.site.register(Category)