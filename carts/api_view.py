from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Cart, CartItem
from .serializer import CartItemSerializer , CartItemDecrementSerializer
from products.models import Product, Variation
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

class AddToCart(APIView):
    def post(self, request, product_id):
        data = request.data.copy()
        data['product_id'] = product_id
        
        serializer = CartItemSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DecrementCart(APIView):
    def post(self, request, product_id, cart_item_id):
        product = get_object_or_404(Product, id=product_id)
        
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
                
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                serializer = CartItemDecrementSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteCartItem(APIView):
    def post(self, request, product_id, cart_item_id):
        product = get_object_or_404(Product, id=product_id)
        
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            
            cart_item.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

# class CartAPI(APIView):
#     def get(self, request):
#         total = 0
#         quantity = 0
#         tax = 0
#         grand_total = 0
#         cart_items = None
        
#         try:
#             if request.user.is_authenticated:
#                 cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#             else:
#                 cart = Cart.objects.get(cart_id=_cart_id(request))
#                 cart_items = CartItem.objects.filter(cart=cart, is_active=True)
                
#             for cart_item in cart_items:
#                 total += (cart_item.product.price * cart_item.quantity)
#                 quantity += cart_item.quantity
            
#             tax = (2 * total) / 100
#             grand_total = total + tax
            
#         except ObjectDoesNotExist:
#             pass
        
#         serializer = CartItemSerializer(cart_items, many=True)
        
#         data = {
#             'total': total,
#             'quantity': quantity,
#             'cart_items': serializer.data,
#             'tax': tax,
#             'grand_total': grand_total
#         }
        
#         return Response(data)