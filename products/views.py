from django.shortcuts import render , get_object_or_404
from .models import Product , Category , Subcategory , Brand
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def product_list(request , subcategory_id=None , brand_slug=None):
    categories = None
    brands = None
    if subcategory_id != None :
        categories = get_object_or_404(Subcategory,id = subcategory_id)
        products = Product.objects.filter(subcategory=categories  ,is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    elif brand_slug != None:
        brands = get_object_or_404(Brand,slug=brand_slug)
        products = Product.objects.filter(PRDBrand=brands ,is_available=True )
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    else :
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    

    context={
        'products':paged_product,
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