from django.shortcuts import render , get_object_or_404
from .models import Product , Category , Subcategory , Brand
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models.query_utils import Q
from .filters import ProductFilter

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
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
        f = ProductFilter(request.GET, queryset=Product.objects.filter())
    

    context={
        'products':paged_product,
        'filter':f,
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

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q :
            product = Product.objects.order_by('-created_at').filter(
                Q(description__icontains=q ) |
                Q( name__icontains=q)|
                Q(subcategory__name__icontains=q)|
                Q(PRDBrand__BRDName__icontains=q)
                )
            product_count = product.count()
        else :
            return render(request , 'products/product_list.html')
    context = {
        'products':product , 
        'product_count':product_count
    }
    return render(request , 'products/product_list.html', context)