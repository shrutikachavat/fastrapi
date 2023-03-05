from django.shortcuts import render
from . import models
from . import serializers
from rest_framework import viewsets

# Create your views here.


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ItemRate.objects.all().order_by('id')
    serializer_class = serializers.ItemRateSerializer
