from products.models import Product
def counter(request):
    product_count = 0
    if request.user.is_authenticated:
        if 'admin' in request.path:
            return{}
        else :
            
            try :
                user_favourites = Product.objects.filter(like=request.user)
                product_count = user_favourites.count()

            except Product.DoesNotExist:
                product_count=0

    return dict(product_count=product_count)