from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'api'

urlpatterns = [
    path('brands/', views.brand_list, name='barand_list'),
    path('brands/insert', views.brand_insert, name='barand_insert'),
    path('chickens/', views.chicken_list, name='chicken_list'),
    path('chickens/insert', views.chicken_insert, name='chicken_insert'),
]