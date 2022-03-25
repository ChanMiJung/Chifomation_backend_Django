from django.db import models
from django.conf import settings

# Create your models here.
class Brand(models.Model):
    name = models.TextField()
    img_url = models.TextField(blank=True)



class Chicken(models.Model):
    name = models.TextField()
    cost = models.IntegerField()
    category = models.TextField(blank=True)
    img_url = models.TextField(blank=True)
    original_category = models.TextField()
    introduction = models.TextField(blank=True)
    hash_tag = models.TextField(blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    new = models.BooleanField(default=False)
    popularity = models.BooleanField(default=False)


class Comment(models.Model):
    content = models.TextField()
    star = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE)