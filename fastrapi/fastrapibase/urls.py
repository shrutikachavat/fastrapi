from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()


urlpatterns = [
    # path('', views.HomeAPIView.as_view()),
    # path('fastrkart/kart/', views.FastrkartDetailsAPIView.as_view(), name=["fastrkart_kart"]),
    path('', views.FastrkartDetailsAPIView.as_view()),
    path('fastrkart/product/add/<int:pk>', views.FastrkartAddAPIView.as_view()),
    path('fastrkart/product/remove/<int:pk>', views.FastrkartRemoveAPIView.as_view()),
    # path('fastrkart/product/<int:pk>', views.FastrkartViewSet.as_view({'post':'create','delete':'remove'})),
    path('product/products/<int:pk>', views.ProductViewSet.as_view({'get':'retrieve'})),
    path('product/products/', views.ProductPaginatedViewSet.as_view()),
    # path('', views.ProductPaginatedViewSet.as_view()),
]