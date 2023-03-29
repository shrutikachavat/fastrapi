from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()


urlpatterns = [
    # path('', views.HomeAPIView.as_view()),
    # path('fastrkart/kart/', views.FastrkartDetailsAPIView.as_view(), name=["fastrkart_kart"]),
    path('', views.FastrkartDetailsAPIView.as_view()),
    path('fastrkart/product/add/', views.FastrkartAddAPIView.as_view()),
    path('fastrkart/product/remove/', views.FastrkartRemoveAPIView.as_view()),
    # product
    path('product/products/<int:pk>', views.ProductViewSet.as_view({'get':'retrieve'})),
    path('product/products/', views.ProductPaginatedViewSet.as_view()),
    # path('', views.ProductPaginatedViewSet.as_view()),
    # user
    path('user/user/', views.ManageUserView.as_view()),
    path('user/user/', views.CreateUserAPIView.as_view()),
    # token
    path('token/create/', views.CreateTokenView.as_view()),
    # path('token/fetch/' views.FetchTokenView.as_view()),
]