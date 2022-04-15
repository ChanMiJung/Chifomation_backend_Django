from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signIn/', views.signIn, name='signIn'),
    path('signUp/', views.signUp, name='signUp'),
    path('signOut/', views.signOut, name='signOut'),
    path('update/', views.update, name='update'),
    path('profile/', views.profile, name='profile'),
    path('check_username', views.check_username, name='check_username'),
    path('check_nickname', views.check_nickname, name='check_nickname'),
    path('check_user_info', views.check_user_info, name='check_user_info'),
    path('confirm_authenticate', views.confirm_authenticate, name='confirm_authenticate'),
]