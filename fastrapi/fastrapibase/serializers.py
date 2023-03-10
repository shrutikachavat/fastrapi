from rest_framework import serializers
from . import models


class ProductPriceSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = models.ProductPrice