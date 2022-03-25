from rest_framework import serializers
from .models import Brand, Chicken


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'img_url']


class ChickenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chicken
        fields = ['id', 'name', 'cost', 'category', 'img_url', 'original_category', 'introduction', 'hash_tag', 'brand', 'new', 'popularity']