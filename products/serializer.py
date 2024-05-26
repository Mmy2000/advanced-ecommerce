from rest_framework import serializers
from .models import Product , Subcategory , Category , Brand 
from taggit.models import Tag
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


class SubcategorySerializer(serializers.ModelSerializer):
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


class ProductsSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer()
    PRDBrand = BrandSerializer()
    tags = TagListSerializerField()
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
