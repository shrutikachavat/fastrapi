from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from . import models
from . import serializers
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.generics import GenericAPIView
# import requests
import serial
from .fastrkart import Fastrkart
# from .management.commands import arduino

# Create your views here.

class ProductViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        queryset = models.ProductRate.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProductRateSerializer(product)
        return Response(serializer.data)


class FastrkartDetailsAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        auth_token = request.COOKIES.get("auth_token")
        # token, created = Token.objects.get_or_create(key=auth_token)
        if auth_token:
            token = serializers.AuthTokenSerializer(auth_token)
            if token.is_valid:
                kart = Fastrkart(request)
                return render(request,
                              context={"data": kart},
                              template_name='fastrapibase/index.html')
            else:
                return render(request,
                              template_name='fastrapibase/login.html')
        else:
            return render(request,
                          template_name='fastrapibase/login.html')
    
class FastrkartAddAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
          OpenApiParameter("tag_id", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
          OpenApiParameter("quantity", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False)
        ]
    )
    def post(self, request, quantity=1):
        # if request.user.is_authenticated:
            tag_id = request.query_params.get("tag_id", None)
            quantity = request.query_params.get("quantity", quantity)
            kart = Fastrkart(request)
            product = get_object_or_404(models.ProductRate, tag_id=tag_id)
            kart.fastrkart_add(product=product, quantity=quantity)
            return render(request,
                          context={"data":kart},
                          template_name="fastrapibase/index.html")
        # else:
        #     return render(request,
        #                   template_name='fastrapibase/login.html')
    
class FastrkartRemoveAPIView(GenericAPIView):
    template_classes = [TemplateHTMLRenderer]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter("tag_id", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("quantity", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False)
        ]
    )
    def delete(self, request, quantity=1):
        # if request.user.is_authenticated:
            tag_id = request.query_params.get("tag_id", None)
            quantity = request.query_params.get("quantity", quantity)
            kart = Fastrkart(request)
            product = get_object_or_404(models.ProductRate, tag_id=tag_id)
            kart.fastrkart_remove(product=product, quantity=quantity)
            return render(request,
                        context={"data":kart},
                        template_name="fastrapibase/index.html")
        # else:
        #     return render(request,
        #                   template_name='fastrapibase/login.html')

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
    authentication_classes = [authentication.TokenAuthentication]
    # renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            if user.is_authenticated:
                response = HttpResponseRedirect(redirect_to=reverse('kart'))
                response.set_cookie(key="auth_token",
                                    value=f"Token {token.key}")
                # response.headers["Authorization"] = f"Token {token.key}"
                return response
            else:
                return redirect(reverse('kart'))
        except Exception:
            return redirect(reverse('kart'))
            # return render(request,
            #               template_name='fastrapibase/login.html')

    # def post(self, request):
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid()
    #         user = serializer.validated_data['user']
    #     except Exception as e:
    #         return redirect('kart')
    #     else:
    #         token, created = Token.objects.get_or_create(user=user)
    #         data = {"token":f"{token.key}"}
    #         header = {"Authorization":f"Token {token.key}"}
    #         return Response(data=data,
    #                         headers=header)

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class ArduinoAPIView(GenericAPIView):

    def rfid_card_present():
        ser = serial.Serial()
        ser.baudrate = settings.ARDUINO_BAUDRATE
        ser.port = settings.ARDUINO_PORT
        ser.open()
        raw_data = ser.readline()
        if raw_data:
            raw_data = raw_data.decode()
            raw_data = raw_data.strip()
            return raw_data

    def tag_id_provider(tag_id):
        return tag_id

    def get(self):
        RFID_DATA = self.rfid_card_present()
        if RFID_DATA:
            tag_id = ArduinoAPIView.tag_id_provider(RFID_DATA)
            print(tag_id)
        else:
            print('NO RFID')