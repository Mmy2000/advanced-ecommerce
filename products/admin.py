from django.contrib import admin
from .models import Product , Category , Subcategory , Brand , ProductImages
# Register your models here.

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price'  , 'subcategory' , 'PRDBrand' , 'stock' , 'created_at' , 'is_available')

admin.site.register(Product , ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory , SubCategoryAdmin)
admin.site.register(Brand)
admin.site.register(ProductImages)