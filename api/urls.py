from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'api'

urlpatterns = [
    path('chickens/', views.chicken_list, name='chicken_list'),
]