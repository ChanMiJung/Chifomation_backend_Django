from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    userID = models.CharField(max_length=20)    
    phoneNum = models.CharField(max_length=13, blank=True)
    nickname = models.CharField(max_length=40)