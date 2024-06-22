from django import forms
from .models import ReviewRating
from .models import  Subcategory


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject' , 'review' , 'rating']


# forms.py



