from rest_framework import serializers
from .models import Product , Subcategory , Category , Brand
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer()
    PRDBrand = BrandSerializer()
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
