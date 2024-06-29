from products.models import Subcategory , Category
from django.db.models import Count

def category_nav(request):
    categories = Category.objects.all().annotate(subcategory_count=Count('subcategory'))
    subcategories = Subcategory.objects.all()
    
    context = {
        'subcategories':subcategories,
        'categories':categories,
    }
    return context