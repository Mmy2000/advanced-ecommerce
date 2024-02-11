from django.shortcuts import render
from .models import Product
# Create your views here.
def product_list(request):
    products = Product.objects.all()
    context={
        'products':products
    }
    return render(request , 'products/product_list.html' , context )

def product_detail(request ,product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        single_product.views+=1
        single_product.save()
        related = Product.objects.filter(subcategory=single_product.subcategory)
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'related':related,
    }
    return render(request , 'products/product_detail.html' , context)