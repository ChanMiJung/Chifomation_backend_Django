from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BrandSerializer, ChickenSerializer, CategorySerializer
from .models import Brand, Chicken, Category

# Create your views here.
@api_view(['GET'])
def brand_list(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def brand_insert(request):
    serializer = BrandSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def category_list(request):
    brands = Category.objects.all()
    serializer = CategorySerializer(brands, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def category_insert(request):
    serializer = CategorySerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def brand_update(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    serializer = BrandSerializer(brand, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(Serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def chicken_list(request):
    chickens = Chicken.objects.all()
    serializer = ChickenSerializer(chickens, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def chicken_insert(request):
    data = request.data
    if Brand.objects.filter(name=data['brand']).exists():
        brand = Brand.objects.get(name=data['brand']).id
        data['brand'] = brand
        serializer = ChickenSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def chicken_update(request, chicken_id):
    chicken = get_object_or_404(Chicken, pk=chicken_id)
    serializer = ChickenSerializer(chicken, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    

