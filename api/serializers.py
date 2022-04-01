from rest_framework import serializers
from .models import Brand, Category, Chicken


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'img_url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class ChickenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chicken
        fields = ['id', 'name', 'cost', 'category', 'img_url', 'original_category', 'introduction', 'hash_tag', 'brand', 'new', 'popularity']