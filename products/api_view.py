from .models import Product , Subcategory , Category , Brand , Variation , ReviewRating
from taggit.models import Tag
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductsSerializer , SubcategorySerializer , CategorySerializer , BrandSerializer , TagsSerializer , VariationSerializer , ReviewSerializer2
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models.query_utils import Q
from rest_framework.views import APIView
from rest_framework import status


# class ProductListApi(generics.ListCreateAPIView):
#     serializer_class = ProductsSerializer
#     queryset = Product.objects.all()
#     # permission_classes = [IsAuthenticated,]

# class ProsuctDetailsApi(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductsSerializer
#     queryset = Product.objects.all()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    all_products = Product.objects.all()
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_deatils_api(request , id):
    product = get_object_or_404(Product , id=id)
    data = ProductsSerializer(product,context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def subcategory_api(request):
    subcategory = Subcategory.objects.all()
    data = SubcategorySerializer(subcategory , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_api(request):
    category = Category.objects.all()
    data = CategorySerializer(category , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tags_api(request):
    tag = Tag.objects.all()
    data = TagsSerializer(tag , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def brand_api(request):
    brand = Brand.objects.all()
    data = BrandSerializer(brand , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_api(request , query):
    product = Product.objects.filter(
        Q(name__icontains=query)|Q(description__icontains=query)|Q(subcategory__name__icontains=query)
        
    )
    data = ProductsSerializer(product ,many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchByCategory(request , query):
    product = Product.objects.filter(
        Q(subcategory__category__name__icontains=query)
    )
    data = ProductsSerializer(product , many=True , context={'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllSubcategoriesInCategories(request , query):
    product = Subcategory.objects.filter(
        Q(category__name__icontains=query)
    )
    data = SubcategorySerializer(product , many=True , context={'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchBySubcategory(request , query):
    product = Product.objects.filter(
        Q(subcategory__name__icontains=query)
    )
    data = ProductsSerializer(product , many=True , context={'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchByBrand(request , query):
    product = Product.objects.filter(
        Q(PRDBrand__BRDName__icontains=query)
    )
    data = ProductsSerializer(product , many=True , context={'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchByTag(request , query):
    post = Product.objects.filter(
        Q(tags__name__icontains = query)
    )
    data = ProductsSerializer(post , many=True ,context={'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list_ordered_by_review_api(request):
    all_products = Product.objects.all().order_by('reviewrating')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list_ordered_by_createdAt_api(request):
    all_products = Product.objects.all().order_by('-created_at')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list_ordered_by_papularty_api(request):
    all_products = Product.objects.all().order_by('-views')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list_ordered_by_price_api(request):
    all_products = Product.objects.all().order_by('price')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list_ordered_by_price2_api(request):
    all_products = Product.objects.all().order_by('-price')
    data = ProductsSerializer(all_products , many=True , context = {'request':request}).data
    return Response({'data':data} , status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list_api_filter(request):
    products = Product.objects.filter(is_available=True)
    variation_name = request.GET.get('variation_name')

    if variation_name:
        products = products.filter(product_variation__variation_value__icontains=variation_name)

    
    serializer = ProductsSerializer(products, many=True).data
    return Response({'data':serializer}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_by_price_api(request):
    products = Product.objects.filter(is_available=True)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    serializer = ProductsSerializer(products, many=True).data
    return Response({'data':serializer} , status=status.HTTP_200_OK)

class AddToFavouriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        user = request.user
        if user in product.like.all():
            product.like.remove(user)
            message = 'Removed from favourites'
        else:
            product.like.add(user)
            message = 'Added to favourites'
        return Response({'message': message}, status=status.HTTP_200_OK)

@api_view(['GET'])    
def variations(request):
    variation = Variation.objects.all()
    data = VariationSerializer(variation  , many=True).data
    return Response({'data':data} , status=status.HTTP_200_OK)

class SubmitReview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, product_id):
        try:
            review = ReviewRating.objects.get(user=request.user, product_id=product_id)
            serializer = ReviewSerializer2(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Thank You, Your Review has been updated.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReviewRating.DoesNotExist:
            serializer = ReviewSerializer2(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, product_id=product_id)
                return Response({'detail': 'Thank You, Your Review has been submitted.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)