from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Cart, CartItem
from .serializer import CartItemSerializer , CartItemDecrementSerializer , CartItemsSerializer
from products.models import Product, Variation
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
import requests



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        data = request.data.copy()
        data['product_id'] = product_id
        
        serializer = CartItemSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            cart_data = serializer.save()
            return Response(cart_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DecrementCart(APIView):
    permission_classes = [IsAuthenticated]

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
            else:
                cart_item.delete()
            
            # Call the CartAPIView to get the updated cart data
            cart_api_url = reverse('cart_api')  # Assuming 'cart-api' is the name of your CartAPIView URL
            cart_api_url = request.build_absolute_uri(cart_api_url)
            response = requests.get(cart_api_url, headers={'Authorization': request.headers.get('Authorization')})
            
            if response.status_code == 200:
                updated_cart_data = response.json()
                # Process the updated cart data as needed
                return Response({"message": "Product quantity decremented successfully", "updated_cart": updated_cart_data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to retrieve updated cart data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

        

class DeleteCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, cart_item_id):
        product = get_object_or_404(Product, id=product_id)
        
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            
            cart_item.delete()
            
            # Call the CartAPIView to get the updated cart data
            cart_api_url = reverse('cart_api')  # Assuming 'cart-api' is the name of your CartAPIView URL
            cart_api_url = request.build_absolute_uri(cart_api_url)
            response = requests.get(cart_api_url, headers={'Authorization': request.headers.get('Authorization')})
            
            if response.status_code == 200:
                updated_cart_data = response.json()
                # Process the updated cart data as needed
                return Response({"message": "Product deleted successfully", "updated_cart": updated_cart_data}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Failed to retrieve updated cart data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0

        try:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity

            tax = (2 * total) / 100
            grand_total = total + tax

        except ObjectDoesNotExist:
            # Handle the case where no cart items are found for the user
            # You might want to return an empty response or a specific message
            return Response({'detail': 'No cart items found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemsSerializer(cart_items, many=True)
        
        data = {
            'total': total,
            'quantity': quantity,
            'cart_items': serializer.data,
            'tax': tax,
            'grand_total': grand_total
        }

        return Response(data, status=status.HTTP_200_OK)
    
class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0

        try:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity

            tax = (2 * total) / 100
            grand_total = total + tax

        except ObjectDoesNotExist:
            # Handle the case where no cart items are found for the user
            # You might want to return an empty response or a specific message
            return Response({'detail': 'No cart items found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemsSerializer(cart_items, many=True)
        
        data = {
            'total': total,
            'quantity': quantity,
            'cart_items': serializer.data,
            'tax': tax,
            'grand_total': grand_total
        }

        return Response(data, status=status.HTTP_200_OK)