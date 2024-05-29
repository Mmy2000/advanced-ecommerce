from rest_framework import serializers
from .models import Settings , Post , Category , NewsLitter , Contact
from taggit.models import Tag
from taggit.serializers import (TagListSerializerField, TaggitSerializer)



class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagListSerializerField()
    class Meta:
        model = Post
        fields = '__all__'

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLitter
        fields = ['name' , 'email']