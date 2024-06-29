from django.contrib import admin
from .models import Product  , Subcategory  , ProductImages , Variation , ReviewRating , Category
import admin_thumbnails
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGallaryInline(admin.TabularInline):
    model = ProductImages
    extra = 1
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category')

class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    list_display = ('id' , 'name' , 'price' , 'avr_review' , 'count_review' , 'subcategory','get_category'   , 'stock','views' , 'created_at' , 'is_available')
    list_editable = ('is_available',)
    list_filter = ('price' , 'subcategory', 'name','stock')
    def get_category(self, obj):
        return obj.subcategory.category
    
    get_category.short_description = 'Category'

    inlines = [ProductGallaryInline] 



class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user' , 'product' , 'subject' , 'review' , 'rating' , 'status' )
    list_editable = ('status',)
    list_filter = ('product' , 'user' , 'rating')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('id' , 'product' , 'variation_category' , 'variation_value' , 'created_at' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Product  ,SomeModelAdmin)
admin.site.register(Subcategory , SubCategoryAdmin)
admin.site.register(Category)
admin.site.register(ReviewRating , ReviewsAdmin)
admin.site.register(ProductImages)

# admin.site.register(Variation , VariationAdmin)