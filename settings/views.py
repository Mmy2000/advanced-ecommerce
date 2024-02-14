from django.shortcuts import render
from products.models import Product

# Create your views here.
def home(request):
    trandy_paroduct = Product.objects.all().order_by('-views')
    just_arrived = Product.objects.all().order_by('-created_at')

    context = {
        'trandy_product':trandy_paroduct,
        'just_arrived':just_arrived
    }
    return render(request , 'home.html' , context)