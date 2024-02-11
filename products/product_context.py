from products.models import Category , Subcategory

def category_nav(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return context