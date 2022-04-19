from rest_framework.request import Request
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BrandSerializer, ChickenSerializer, CategorySerializer
from .models import Brand, Chicken, Category
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.generics import GenericAPIView

# Create your views here.
class BrandListView(ListModelMixin, GenericAPIView):
    queryset = Brand.objects.order_by('-id')
    serializer_class = BrandSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# @api_view(['GET'])
# def brand_list(request):
#     brands = Brand.objects.all()
#     serializer = BrandSerializer(brands, many=True)
#     return Response(serializer.data)

class BrandDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = Brand.objects.order_by('-id')
    serializer_class = BrandSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class BrandCreateView(CreateModelMixin, GenericAPIView):
    queryset = Brand.objects.order_by('-id')
    serializer_class = BrandSerializer

    def create(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
# @api_view(['POST'])
# def brand_insert(request):
#     serializer = BrandSerializer(data = request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status = status.HTTP_201_CREATED)
#     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# class CategoryListView(ListModelMixin, GenericAPIView):

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
        return Response(BrandSerializer.data)
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
        category = Category.objects.get(name=data['category']).id
        data['category'] = category
        if data['original_category'] == '' and data['category'] != '':
            data['origninal_category'] = data['category']

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

    

