from django import forms
from .models import ReviewRating , Subcategory , ProductImages , Product
from django.forms.models import inlineformset_factory



class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject' , 'review' , 'rating']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['product' , 'image']

ProductImageFormset = inlineformset_factory(
    Product , 
    ProductImages , 
    form = ProductImageForm ,
    fields = ['image'],
    extra=2 , 
    can_delete=True,
)

from taggit.forms import TagField

class ProductForm(forms.ModelForm):
    tags = TagField(required=False,help_text="A comma-separated list of tags.")

    class Meta:
        model = Product
        exclude = ('slug', 'owner', 'is_available', 'like', 'views')



