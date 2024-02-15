from django.shortcuts import render
from products.models import Product , Subcategory
from django.db.models import Count
# Create your views here.
def home(request):
    trandy_paroduct = Product.objects.all().order_by('-views')
    just_arrived = Product.objects.all().order_by('-created_at')
    categories = Subcategory.objects.all().annotate(category_count=Count("product_subcategory"))

    context = {
        'trandy_product':trandy_paroduct,
        'just_arrived':just_arrived,
        'categories':categories,
    }
    return render(request , 'home.html' , context)