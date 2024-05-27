from .models import Product , Subcategory , Category , Brand 
from taggit.models import Tag
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductsSerializer , SubcategorySerializer , CategorySerializer , BrandSerializer , TagsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models.query_utils import Q


# class ProductListApi(generics.ListCreateAPIView):
#     serializer_class = ProductsSerializer
#     queryset = Product.objects.all()
#     # permission_classes = [IsAuthenticated,]

# class ProsuctDetailsApi(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductsSerializer
#     queryset = Product.objects.all()


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
def tags_api(request):
    tag = Tag.objects.all()
    data = TagsSerializer(tag , many=True , context = {'request':request}).data
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

@api_view(['GET'])
def searchBySubcategory(request , query):
    product = Product.objects.filter(
        Q(subcategory__name__icontains=query)
    )
    data = ProductsSerializer(product , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def searchByBrand(request , query):
    product = Product.objects.filter(
        Q(PRDBrand__BRDName__icontains=query)
    )
    data = ProductsSerializer(product , many=True , context={'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def searchByTag(request , query):
    post = Product.objects.filter(
        Q(tags__name__icontains = query)
    )
    data = ProductsSerializer(post , many=True ,context={'request':request}).data
    return Response({'data':data})


@api_view(['GET'])
def product_list_ordered_by_review_api(request):
    all_products = Product.objects.all().order_by('reviewrating')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def product_list_ordered_by_createdAt_api(request):
    all_products = Product.objects.all().order_by('-created_at')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def product_list_ordered_by_papularty_api(request):
    all_products = Product.objects.all().order_by('-views')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def product_list_ordered_by_price_api(request):
    all_products = Product.objects.all().order_by('price')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data})

@api_view(['GET'])
def product_list_ordered_by_price2_api(request):
    all_products = Product.objects.all().order_by('-price')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data})


@api_view(['GET'])
def product_list_api_filter(request):
    products = Product.objects.filter(is_available=True)
    variation_name = request.GET.get('variation_name')

    if variation_name:
        products = products.filter(variation__variation_value__icontains=variation_name)

    
    serializer = ProductsSerializer(products, many=True).data
    return Response({'data':serializer})


@api_view(['GET'])
def filter_by_price_api(request):
    products = Product.objects.filter(is_available=True)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    serializer = ProductsSerializer(products, many=True).data
    return Response({'data':serializer})