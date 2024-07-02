import django_filters
from .models import Product
from django_filters.widgets import RangeWidget
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel
import django_filters
from django.utils.translation import gettext_lazy as _
from .models import Product
from modeltranslation.utils import build_localized_fieldname

lang = 'en'  # Example language code, replace with your logic to get the language code

class ProductFilter(django_filters.FilterSet):
 
    price = django_filters.RangeFilter(
        label=_('Enter Price Range from low to high'),
        field_name='translations__price',
        widget=django_filters.widgets.RangeWidget(attrs={
            'placeholder': _('Enter price range')
        })
    )
    
    name = django_filters.CharFilter(
        field_name='translations__name',
        lookup_expr='icontains',
        label=_('Product Name'),
    )
    
    description = django_filters.CharFilter(
        field_name='translations__description',
        lookup_expr='icontains',
        label=_('Product Description'),
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'subcategory', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.distinct()



from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product

class ArabicTranslationFilter(admin.SimpleListFilter):
    title = _('Arabic Translation')
    parameter_name = 'arabic_translation'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(translations__language_code='ar')
        if self.value() == 'no':
            return queryset.exclude(translations__language_code='ar')
        return queryset