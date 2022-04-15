from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.list, name='list'),
    path('search', views.search, name='search'),
    path('detail/<int:chicken_id>', views.detail, name='detail'),
    path('enroll_comment', views.enroll_comment, name='enroll_comment'),
    path('get_comments', views.get_comments, name='get_comments'),
]