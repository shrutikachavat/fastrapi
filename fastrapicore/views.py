from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.

class ProductViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.ProductRate.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProductRateSerializer(product)
        return Response(serializer.data)