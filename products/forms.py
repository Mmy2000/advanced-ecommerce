from django import forms
from .models import ReviewRating , Subcategory , ProductImages , Product
from django.forms.models import inlineformset_factory
from django_summernote.widgets import SummernoteWidget
from parler.forms import TranslatableModelForm




class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject' , 'review' , 'rating']


class CategoryForm(TranslatableModelForm):
    class Meta:
        model = Subcategory
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label=Subcategory._meta.get_field('name').verbose_name)
        # You can customize other aspects of the field here if needed
        # For example, setting initial value, widget, etc.

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
        }



