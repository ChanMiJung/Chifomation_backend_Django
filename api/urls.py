from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

app_name = 'api'

urlpatterns = [
    path('brands/', views.brand_list, name='barand_list'),
    path('brands/insert', views.brand_insert, name='barand_insert'),
    path('brands/update/<int:brand_id>', views.brand_update, name='barand_update'),
    path('chickens/', views.chicken_list, name='chicken_list'),
    path('chickens/insert', views.chicken_insert, name='chicken_insert'),
    path('chickens/update/<int:chicken_id>', views.chicken_update, name='chicken_update'),
]