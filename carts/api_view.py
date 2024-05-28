from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Cart, CartItem
from .serializer import CartItemSerializer , CartItemDecrementSerializer
from products.models import Product, Variation
from django.shortcuts import get_object_or_404


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