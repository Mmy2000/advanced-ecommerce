from django.shortcuts import render
from products.models import Product

# Create your views here.
def home(request):
    trandy_paroduct = Product.objects.all().order_by('-views')

    context = {
        'trandy_product':trandy_paroduct
    }
    return render(request , 'home.html' , context)