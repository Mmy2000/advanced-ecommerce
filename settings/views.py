from django.shortcuts import render
from products.models import Product , Subcategory
from django.db.models import Count
# Create your views here.
def home(request):
    trandy_paroduct = Product.objects.all().order_by('-views')
    just_arrived = Product.objects.all().order_by('-created_at')
    category = Subcategory.objects.all().annotate(category_count=Count("product_subcategory"))[:3]

    context = {
        'trandy_product':trandy_paroduct,
        'just_arrived':just_arrived,
        'category':category,
    }
    return render(request , 'home.html' , context)

def contact(request):
    return render(request,'contact.html')