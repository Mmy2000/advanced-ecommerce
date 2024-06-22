from products.models import Subcategory 

def category_nav(request):
    subcategories = Subcategory.objects.all()
    context = {
        'subcategories':subcategories,
    }
    return context