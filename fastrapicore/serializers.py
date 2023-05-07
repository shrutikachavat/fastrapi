from rest_framework import serializers
from . import models


class ProductRateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = models.ProductRate