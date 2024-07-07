from django.contrib import admin
from .models import Product, Subcategory, ProductImages, Variation, ReviewRating, Category
import admin_thumbnails
from django_summernote.admin import SummernoteModelAdmin
from parler.admin import TranslatableAdmin
from .filters import ArabicTranslationFilter  # Import the custom filter
from django import forms
from django_summernote.widgets import SummernoteWidget
from modeltranslation.forms import TranslationModelForm


@admin_thumbnails.thumbnail('image')
class ProductGallaryInline(admin.TabularInline):
    model = ProductImages
    extra = 1

class ProductAdminForm(TranslationModelForm):
    description = forms.CharField(widget=SummernoteWidget(), required=True)
    
    class Meta:
        model = Product
        fields = '__all__'

    


class SubCategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'category')

class SomeModelAdmin(TranslatableAdmin, SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ('id', 'get_name', 'price', 'avr_review', 'count_review', 'subcategory', 'get_category', 'stock', 'views', 'created_at', 'is_available')
    list_editable = ('is_available',)
    list_filter = ('translations__price', 'subcategory', 'translations__name', 'translations__stock', ArabicTranslationFilter)

    def get_category(self, obj):
        return obj.subcategory.category

    get_category.short_description = 'Category'

    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)

    get_name.short_description = 'Product Name'

    inlines = [ProductGallaryInline]



class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'subject', 'review', 'rating', 'status')
    list_editable = ('status',)
    list_filter = ('product', 'user', 'rating')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'variation_category', 'variation_value', 'created_at', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, SomeModelAdmin)
admin.site.register(Subcategory, SubCategoryAdmin)
admin.site.register(Category, TranslatableAdmin)
admin.site.register(ReviewRating, ReviewsAdmin)
admin.site.register(ProductImages)


# admin.site.register(Variation , VariationAdmin)