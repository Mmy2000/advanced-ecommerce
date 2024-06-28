from django import forms
from .models import ReviewRating , Subcategory , ProductImages , Product
from django.forms.models import inlineformset_factory
from django_summernote.widgets import SummernoteWidget



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
    extra=3 , 
    can_delete=True,
)

from taggit.forms import TagField

class ProductForm(forms.ModelForm):
    tags = TagField(required=False,help_text="A comma-separated list of tags.")
    created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Product
        exclude = ('slug', 'owner', 'is_available', 'like', 'views')
        widgets = {
            'description': SummernoteWidget(),
            'features': SummernoteWidget(),
        }



