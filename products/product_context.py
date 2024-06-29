from products.models import Subcategory , Category

def category_nav(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    context = {
        'subcategories':subcategories,
        'categories':categories,
    }
    return context