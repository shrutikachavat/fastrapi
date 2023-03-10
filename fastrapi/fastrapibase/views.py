from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

# Create your views here.

# def home(request):
#     return render(request, 'fastr/index.html')

class HomeAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(status=status.HTTP_200_OK,
                        template_name='fastrapibase/index.html')

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ProductPrice.objects.all().order_by('id')
    serializer_class = serializers.ProductPriceSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 5

class ProductPaginatedViewSet(ListAPIView):
    queryset = models.ProductPrice.objects.all()
    serializer_class = serializers.ProductPriceSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response({"ProductPriceList": self.get_queryset() }, 
                        template_name='fastrapibase/index.html')