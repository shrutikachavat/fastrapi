from rest_framework import serializers
from . import models


class ItemRateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = models.ItemRate