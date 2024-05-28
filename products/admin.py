from django.contrib import admin
from .models import Product , Category , Subcategory , Brand , ProductImages , Variation , ReviewRating , Coupon
import admin_thumbnails

# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGallaryInline(admin.TabularInline):
    model = ProductImages
    extra = 1
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name' , 'price' , 'avr_review' , 'count_review' , 'discount' , 'subcategory' , 'get_category' , 'PRDBrand' , 'stock','views' , 'created_at' , 'is_available')
    list_editable = ('is_available',)
    list_filter = ('price' , 'subcategory' , 'name','stock','PRDBrand' , 'discount' )
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

admin.site.register(Product , ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory , SubCategoryAdmin)
admin.site.register(Brand)
admin.site.register(ReviewRating , ReviewsAdmin)
admin.site.register(ProductImages)
admin.site.register(Variation,VariationAdmin)
admin.site.register(Coupon)