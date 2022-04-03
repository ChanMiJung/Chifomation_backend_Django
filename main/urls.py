from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.list, name='list'),
    path('search', views.search, name='search'),
]