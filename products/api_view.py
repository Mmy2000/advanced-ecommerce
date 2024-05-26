from .models import Product , Subcategory , Category , Brand
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductsSerializer , SubcategorySerializer , CategorySerializer , BrandSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models.query_utils import Q

class NotesListApi(generics.ListCreateAPIView):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()
    # permission_classes = [IsAuthenticated,]

class NotesDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()


@api_view(['GET'])
def product_list(request):
    all_products = Product.objects.all()
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def product_deatils_api(request , id):
    product = get_object_or_404(Product , id=id)
    data = ProductsSerializer(product,context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def subcategory_api(request):
    subcategory = Subcategory.objects.all()
    data = SubcategorySerializer(subcategory , many=True , context = {'request':request}).data
    return Response({'data':data})


@api_view(['GET'])
def category_api(request):
    category = Category.objects.all()
    data = CategorySerializer(category , many=True , context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def brand_api(request):
    brand = Brand.objects.all()
    data = BrandSerializer(brand , many=True , context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def search_api(request , query):
    product = Product.objects.filter(
        Q(name__icontains=query)|Q(description__icontains=query)|Q(subcategory__name__icontains=query)
        
    )
    data = ProductsSerializer(product ,many=True , context = {'request':request}).data
    return Response({'data':data})
@api_view(['GET'])
def searchByCategory(request , query):
    product = Product.objects.filter(
        Q(subcategory__category__name__icontains=query)
    )
    data = ProductsSerializer(product , many=True , context={'request':request}).data
    return Response({'data':data})

# @api_view(['GET'])
# def searchByTag(requset , query):
#     post = Note.objects.filter(
#         Q(tags__name__icontains = query)
#     )
#     data = ProductsSerializer(post , many=True).data
#     return Response({'data':data})