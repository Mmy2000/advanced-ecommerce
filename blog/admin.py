from django.contrib import admin
from .models import Post , Category
from django_summernote.admin import SummernoteModelAdmin
from parler.admin import TranslatableAdmin

# Register your models here.
class PostAdmin(SummernoteModelAdmin,TranslatableAdmin):
    summernote_fields = '__all__'
    list_display = ['title', 'author', 'category', 'created_at', 'views']

admin.site.register(Post, PostAdmin)


admin.site.register(Category)
