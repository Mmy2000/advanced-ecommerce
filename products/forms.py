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

class ProductForm(forms.ModelForm):
    # new_category = forms.CharField(required=False)
    # existing_category = forms.ModelChoiceField(queryset=Subcategory.objects.all(), required=False)

    class Meta:
        model = Product
        exclude = ('slug', 'owner', 'is_available', 'like', 'views')



        # if new_category and existing_category:
        #     raise forms.ValidationError("Please enter either a new category or select an existing category, not both.")

        # if not new_category and not existing_category:
        #     raise forms.ValidationError("Please provide a category.")

