from django.contrib import admin
from .models import Post , Category
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    list_display = ['auther' , 'title','category'  ,'created_at','views']


admin.site.register(Post , SomeModelAdmin)
admin.site.register(Category)