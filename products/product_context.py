from products.models import Category , Subcategory , Brand

def category_nav(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    brands = Brand.objects.all()
    context = {
        'categories':categories,
        'brands':brands,
        'subcategories':subcategories,
    }
    return context