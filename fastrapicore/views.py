from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes


# Create your views here.

class ProductViewSet(viewsets.ViewSet):

    @extend_schema(
        parameters=[
            OpenApiParameter("tag_id", OpenApiTypes.STR, OpenApiParameter.QUERY, required=False),
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False)
        ]
    )
    def retrieve(self, request):
        tag_id = request.query_params.get("tag_id")
        id = request.query_params.get("id")
        queryset = models.ProductRate.objects.all()
        if tag_id:
            product = get_object_or_404(queryset, tag_id=tag_id)
        elif id:
            product = get_object_or_404(queryset, pk=id)
        else:
            return Response(data={"detail": "id or tag_id is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ProductRateSerializer(product)
        return Response(serializer.data)