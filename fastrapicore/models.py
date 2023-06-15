from django.db import models

# Create your models here.
class ProductRate(models.Model):
    tag_id = models.CharField(max_length=16,unique=True)
    brand = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    rate = models.FloatField()
    size = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    material = models.CharField(max_length=255, null=True)
    colour = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)