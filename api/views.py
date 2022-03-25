from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChickenSerializer
from .models import Chicken

# Create your views here.
@api_view(['GET'])
def chicken_list(request):
    chickens = Chicken.objects.all()
    serializer = ChickenSerializer(chickens, many=True)
    print(serializer)
    return Response(serializer.data)