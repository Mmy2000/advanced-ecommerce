import django_filters
from .models import Product
from django_filters.widgets import RangeWidget

class ProductFilter(django_filters.FilterSet):
   
    price = django_filters.RangeFilter(
        label='Enter Price Range from low to high',
        widget=RangeWidget(attrs={
            'placeholder': 'Enter price range'
        })
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'subcategory', 'price']