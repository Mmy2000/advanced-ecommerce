from django import forms
from .models import Product
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['subject' , 'review' , 'rating']