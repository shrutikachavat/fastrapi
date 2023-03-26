from django.shortcuts import render, get_object_or_404
from . import models
from . import serializers
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from rest_framework.generics import GenericAPIView
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

class FastrkartDetailsAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]

    def get(self, request):
        kart = Fastrkart(request)
        return render(request,
                      context={"data": kart},
                      template_name='fastrapibase/index.html')
    
class FastrkartAddAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]

    @extend_schema(
        parameters=[
          OpenApiParameter("quantity", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False)
        ]
    )
    def post(self, request, pk=None, quantity=1):
        quantity = request.query_params.get("quantity", quantity)
        kart = Fastrkart(request)
        product = get_object_or_404(models.ProductRate, id=pk)
        kart.fastrkart_add(product=product, quantity=quantity)
        return render(request,
                      context={"data":kart},
                      template_name="fastrapibase/index.html")
    
class FastrkartRemoveAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]

    @extend_schema(
        parameters=[
            OpenApiParameter("quantity", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False)
        ]
    )
    def delete(self, request, pk=None, quantity=1):
        quantity = request.query_params.get("quantity", quantity)
        kart = Fastrkart(request)
        product = get_object_or_404(models.ProductRate, id=pk)
        kart.fastrkart_remove(product=product, quantity=quantity)
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