from django import forms
from .models import ReviewRating
from .models import Category, Subcategory


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject' , 'review' , 'rating']


# forms.py
import django_filters
from django import forms
from .models import Category, Subcategory, Product

class CategorySubcategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label="Category")
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none(), required=True, label="Subcategory")


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="Category", field_name='subcategory__category', distinct=True, required=False)
    subcategory = django_filters.ModelChoiceFilter(queryset=Subcategory.objects.all(), label="Subcategory", required=False)
    price = django_filters.RangeFilter(field_name='price', label="Price Range")

    class Meta:
        model = Product
        fields = ['name', 'PRDBrand', 'description', 'category', 'subcategory', 'price']

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                if category_id:
                    self.filters['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
                else:
                    self.filters['subcategory'].queryset = Subcategory.objects.filter(category__isnull=True).order_by('name')
            except (ValueError, TypeError):
                self.filters['subcategory'].queryset = Subcategory.objects.none()
        else:
            self.filters['subcategory'].queryset = Subcategory.objects.filter(category__isnull=True).order_by('name')
