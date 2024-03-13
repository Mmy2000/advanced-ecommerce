from django.contrib import admin
from .models import Product , Category , Subcategory , Brand , ProductImages , Variation , ReviewRating
# Register your models here.

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price'  , 'subcategory' , 'get_category' , 'PRDBrand' , 'stock','views' , 'created_at' , 'is_available')

    def get_category(self, obj):
        return obj.subcategory.category
    
    get_category.short_description = 'Category'

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product' , 'variation_category' , 'variation_value' , 'created_at' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Product , ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory , SubCategoryAdmin)
admin.site.register(Brand)
admin.site.register(ReviewRating)
admin.site.register(ProductImages)
admin.site.register(Variation,VariationAdmin)