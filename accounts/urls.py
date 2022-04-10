from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signIn/', views.signIn, name='signIn'),
    path('signUp/', views.signUp, name='signUp'),
    # path('signOut/', views.signOut, name='signOut'),
    # path('update/', views.update, name='update'),
    path('profile/', views.profile, name='profile'),
]