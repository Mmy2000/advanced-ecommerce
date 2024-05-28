from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Cart, CartItem
from .serializer import CartItemSerializer
from products.models import Product, Variation


class AddToCart(APIView):
    def post(self, request, product_id):
        data = request.data.copy()
        data['product_id'] = product_id
        
        serializer = CartItemSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)