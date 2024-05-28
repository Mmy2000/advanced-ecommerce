from rest_framework import serializers
from .models import Product , Subcategory , Category , Brand , ProductImages , ReviewRating , Variation
from taggit.models import Tag
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = '__all__'

class ReviewSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'rating', 'review']

class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Subcategory
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']


class ProductsSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer()
    PRDBrand = BrandSerializer()
    tags = TagListSerializerField()
    reviewrating = ReviewSerializer(many=True, read_only=True)
    product_image = ProductImagesSerializer(many=True, read_only=True)
    product_variation = VariationSerializer(many=True, read_only=True) 
    class Meta:
        model = Product
        fields = '__all__'


