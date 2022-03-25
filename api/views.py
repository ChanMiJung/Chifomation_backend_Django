from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BrandSerializer, ChickenSerializer
from .models import Brand, Chicken

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


