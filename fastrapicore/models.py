from django.db import models

# Create your models here.
class ProductRate(models.Model):
    tag_id = models.CharField(max_length=16,unique=True)
    title = models.CharField(max_length=255)
    rate = models.FloatField()
    size = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)