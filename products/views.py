from django.shortcuts import render , get_object_or_404 , redirect
from .models import Product , Category , Subcategory , Brand , ReviewRating , Variation
from taggit.models import Tag
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Count
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

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
        reviews = ReviewRating.objects.filter(product_id=single_product.id , status=True)
        if request.user.is_authenticated:
            try:
                orderproduct = OrderProduct.objects.filter(user=request.user , product_id=single_product.id).exists()
            except OrderProduct.DoesNotExist:
                orderproduct = None
        else :
            orderproduct = None
        single_product.views+=1
        single_product.save()
        related = Product.objects.filter(subcategory=single_product.subcategory)
        related_count = related.count()
        orderproduct_counter =  OrderProduct.objects.filter( product_id=single_product.id)
        orderproduct_count = orderproduct_counter.count()
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'related':related,
        'related_count':related_count,
        'reviews':reviews,
        'orderproduct':orderproduct,
        'orderproduct_count':orderproduct_count
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


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def search_result(request):
    if is_ajax(request=request):
        product = request.POST.get('product')
        # print(product)
        res = None
        query = Product.objects.filter(
            Q(name__icontains=product) | 
            Q(description__icontains=product) | 
            Q(subcategory__name__icontains=product)|
            Q(subcategory__category__name__icontains=product)|
            Q(PRDBrand__BRDName__icontains=product)
            )
        # print(query)
        if (len(query) > 0 and len(product) > 0):
            data = []
            for pos in query:
                item = {
                    'name':pos.name,
                    'slug':pos.slug,
                    'image':str(pos.image.url),
                    'subcategory':pos.subcategory.id,
                    'price':pos.price,
                    'discount':pos.discount,
                    'rate':pos.count_review(),
                    'avgRate':pos.avr_review()
                    
                }
                data.append(item)
            res = data
            
        else:
            res = "<div class='col-12 my-5 mx-5 text-center'><h2>Nothing Found , PLS Try Again</h2></div>"

        return JsonResponse({'data':res})
    return JsonResponse({})

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
    paged_product = []

    # for product in products:
    if min_price:
            product = products.filter(price__gte=min_price,is_available=True)
            paginator = Paginator(product,6)
            page = request.GET.get('page')
            paged_product = paginator.get_page(page)
            print(product)

    if max_price:
            product = products.filter(price__lte=max_price,is_available=True)
            paginator = Paginator(product,6)
            page = request.GET.get('page')
            paged_product = paginator.get_page(page)

    context = {
        'products':paged_product
    }
    return render(request , 'products/product_list.html', context)

def filter_by_variations(request):
    products = Product.objects.filter(is_available=True)
    variation_name = request.GET.get('variation_name')
    paged_product = []
    if variation_name:
        products = products.filter(variation__variation_value__icontains=variation_name)
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
    context = {
        'products':paged_product
    }
    return render(request , 'products/product_list.html', context)



def submit_review(request , product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method =="POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id , product__id=product_id)
            form = ReviewForm(request.POST , instance=reviews)
            form.save()
            messages.success(request,'Thank You , Your Review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank You , Your Review has been submitted.')
                return redirect(url)
            

def product_list_orderd_by_rating(request):
    products = Product.objects.all().order_by('reviewrating')
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    context = {'products': paged_product,}
    return render(request, 'products/product_list.html', context)

def product_list_orderd_by_created(request):
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    context =  {'products': paged_product,}
    return render(request , 'products/product_list.html' , context)
def product_list_orderd_by_papularty(request):
    products = Product.objects.all().order_by('-views')
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    context =  {'products': paged_product,}
    return render(request , 'products/product_list.html' , context)

def product_list_orderd_by_price(request):
    products = Product.objects.all().order_by('price')
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    context =  {'products': paged_product,}
    return render(request , 'products/product_list.html' , context)

def product_list_orderd_by_price2(request):
    products = Product.objects.all().order_by('-price')
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    context =  {'products': paged_product,}
    return render(request , 'products/product_list.html' , context)