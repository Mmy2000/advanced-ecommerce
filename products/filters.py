import django_filters
from .models import Product
from django_filters.widgets import RangeWidget
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel


class ProductFilter(django_filters.FilterSet):
   
    price = django_filters.RangeFilter(
        label=_('Enter Price Range from low to high'),
        field_name='translations__price',
        widget=RangeWidget(attrs={
            'placeholder': _('Enter price range')
        })
    )
    name = django_filters.CharFilter(
        field_name='translations__name',
        lookup_expr='icontains',
        label=_('Product Name'),
        
    )
    description = django_filters.CharFilter(
        field_name='translations__name',
        lookup_expr='icontains',
        label=_('Product description'),
        
    )

    class Meta:
        model = Product
        fields = ['name','description', 'subcategory', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)