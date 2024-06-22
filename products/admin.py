from django.contrib import admin
from .models import Product  , Subcategory  , ProductImages , Variation , ReviewRating , Coupon
import admin_thumbnails

# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGallaryInline(admin.TabularInline):
    model = ProductImages
    extra = 1
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name' , 'price' , 'avr_review' , 'count_review' , 'subcategory'   , 'stock','views' , 'created_at' , 'is_available')
    list_editable = ('is_available',)
    list_filter = ('price' , 'subcategory' , 'name','stock')

    
    inlines = [ProductGallaryInline] 

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user' , 'product' , 'subject' , 'review' , 'rating' , 'status' )
    list_editable = ('status',)
    list_filter = ('product' , 'user' , 'rating')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('id' , 'product' , 'variation_category' , 'variation_value' , 'created_at' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Product , ProductAdmin)
admin.site.register(Subcategory , SubCategoryAdmin)
admin.site.register(ReviewRating , ReviewsAdmin)
admin.site.register(ProductImages)
# admin.site.register(Variation , VariationAdmin)