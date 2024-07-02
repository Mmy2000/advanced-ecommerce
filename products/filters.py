import django_filters
from .models import Product
from django_filters.widgets import RangeWidget
from django.utils.translation import gettext_lazy as _


class ProductFilter(django_filters.FilterSet):
   
    price = django_filters.RangeFilter(
        label=_('Enter Price Range from low to high'),
        field_name='translations__price',
        widget=RangeWidget(attrs={
            'placeholder': _('Enter price range')
        })
    )

    class Meta:
        model = Product
        fields = ['translations__name', 'translations__description', 'subcategory', 'price']