from django.shortcuts import render , redirect , get_object_or_404
from products.models import Product , Variation
from .models import Cart , CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.filter(variation_category__iexact=key , variation_value__iexact=value)
                print(variation)
            except:
                pass
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product , cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product ,
            cart = cart ,
            quantity = 1
        )
        cart_item.save()
    return redirect('cart')

def decrement_cart(request , product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product , id=product_id)
    cart_item = CartItem.objects.get(product=product , cart = cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def delete_cart(request , product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product , id=product_id)
    cart_item = CartItem.objects.get(product=product , cart = cart)
    cart_item.delete()
    return redirect('cart')

def cart(request , total = 0 , quantity = 0 , cart_items = None):
    
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart , is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total ,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request , 'cart.html' , context)