from products.models import Category , Subcategory 

def category_nav(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    context = {
        'categories':categories,
        'subcategories':subcategories,
    }
    return context