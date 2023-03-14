from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import serializers
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .fastrkart import Fastrkart

# Create your views here.

# def home(request):
#     return render(request, 'fastr/index.html')

# class HomeAPIView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request):
#         return Response(status=status.HTTP_200_OK,
#                         template_name='fastrapibase/index.html')

class ProductViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.ProductRate.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProductRateSerializer(product)
        return Response(serializer.data)
    
# class FastrkartDetailsAPIView(APIView):
#     template_classes = [TemplateHTMLRenderer]

#     def get(request):
#         kart = Fastrkart(request)
#         return render(request,
#                       {'kart':kart},
#                       template_name='fastrapibase/index.html')

class FastrkartViewSet(viewsets.GenericViewSet):
    template_classes = [TemplateHTMLRenderer]

    def retrieve(self, request):
        kart = Fastrkart(request)
        return render(request,
                      context={"data": kart},
                      template_name='fastrapibase/index.html')

    def create(self, request, pk=None):
        kart = Fastrkart(request)
        product = get_object_or_404(models.ProductRate,id=pk)
        kart.fastrkart_add(product=product)
        return render(request,
                      context={"data":kart},
                      template_name="fastrapibase/index.html")
    
    def remove(self, request, pk=None):
        kart = Fastrkart(request)
        product = get_object_or_404(models.ProductRate, id=pk)
        kart.fastrkart_remove(product=product)
        return render(request,
                      context={"data":kart},
                      template_name="fastrapibase/index.html") 

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 5

class ProductPaginatedViewSet(ListAPIView):
    queryset = models.ProductRate.objects.all()
    serializer_class = serializers.ProductRateSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response({"ProductRateList": self.get_queryset() }, 
                        template_name='fastrapibase/index.html')