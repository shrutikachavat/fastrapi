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
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.generics import GenericAPIView
from .fastrkart import Fastrkart

# Create your views here.

class ProductViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.ProductRate.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProductRateSerializer(product)
        return Response(serializer.data)


class FastrkartDetailsAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        kart = Fastrkart(request)
        return render(request,
                      context={"data": kart},
                      template_name='fastrapibase/index.html')
    
class FastrkartAddAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
          OpenApiParameter("tag_id", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
          OpenApiParameter("quantity", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False)
        ]
    )
    def post(self, request, quantity=1):
        tag_id = request.query_params.get("tag_id", None)
        quantity = request.query_params.get("quantity", quantity)
        kart = Fastrkart(request)
        product = get_object_or_404(models.ProductRate, tag_id=tag_id)
        kart.fastrkart_add(product=product, quantity=quantity)
        return render(request,
                      context={"data":kart},
                      template_name="fastrapibase/index.html")
    
class FastrkartRemoveAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("quantity", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False)
        ]
    )
    def delete(self, request, quantity=1):
        tag_id = request.query_params.get("tag_id", None)
        quantity = request.query_params.get("quantity", quantity)
        kart = Fastrkart(request)
        product = get_object_or_404(models.ProductRate, tag_id=tag_id)
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
    
class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

class CreateTokenView(ObtainAuthToken):
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user