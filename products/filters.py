import django_filters
from .models import Product
from django_filters.widgets import RangeWidget
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(
        label=_('Enter Price Range from low to high'),
        widget=RangeWidget(attrs={
            'placeholder': _('Enter price range')
        })
    )

    def filter_translations_name(self, queryset, name, value):
        return queryset.filter(translations__name__icontains=value)

    def filter_translations_description(self, queryset, name, value):
        return queryset.filter(translations__description__icontains=value)

    class Meta:
        model = Product
        fields = ['subcategory', 'price']

    # Override init method to add custom filters dynamically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if TranslatableModel in getattr(self.Meta.model, '__bases__', ()):
            self.filters['translations__name'] = django_filters.CharFilter(
                method='filter_translations_name',
                label=_('Product Name '),
            )
            self.filters['translations__description'] = django_filters.CharFilter(
                method='filter_translations_description',
                label=_('Product Description '),
            )