from django.shortcuts import render , get_object_or_404
from .models import Product , Category , Subcategory , Brand 
from taggit.models import Tag
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.db.models import Count


# Create your views here.
def product_list(request , subcategory_id=None , brand_slug=None , tag_slug=None):
    categories = None
    brands = None
    tags = None
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
    elif tag_slug != None:
        tags = get_object_or_404(Tag , slug = tag_slug)
        products = Product.objects.filter(tags = tags , is_available = True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    else :
        products = Product.objects.filter(is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    

    context={
        'products':paged_product,
    }
    return render(request , 'products/product_list.html' , context )

def product_detail(request ,subcategory_id,product_slug):
    try:
        single_product = Product.objects.get(subcategory_id=subcategory_id,slug=product_slug)
        single_product.views+=1
        single_product.save()
        related = Product.objects.filter(subcategory=single_product.subcategory)
        related_count = related.count()
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'related':related,
        'related_count':related_count
    }
    return render(request , 'products/product_detail.html' , context)
def category_list(request):
    category = Subcategory.objects.all().annotate(category_count=Count("product_subcategory"))
    paginator = Paginator(category,3)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    context = {
        'category':paged_product
    }
    return render(request,'products/categories.html',context)
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

def add_to_favourit(request,id):
    product = Product.objects.get(id=id)
    if request.user in product.like.all():
        product.like.remove(request.user.id)
    else:
        product.like.add(request.user.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def filter_by_price(request):
    products = Product.objects.filter(is_available=True)
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    for product in products:
        if min_price:
                product = products.filter(price__gte=min_price,is_available=True)

        if max_price:
                product = products.filter(price__lte=max_price,is_available=True)

    context = {
        'products':product
    }
    return render(request , 'products/product_list.html', context)

def filter_by_variations(request):
    products = Product.objects.filter(is_available=True)
    variation_name = request.GET.get('variation_name')
    if variation_name:
        products = products.filter(variation__variation_value__icontains=variation_name)
    context = {
        'products':products
    }
    return render(request , 'products/product_list.html', context)