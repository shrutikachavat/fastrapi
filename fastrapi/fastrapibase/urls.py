from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()


urlpatterns = [
    path('', views.HomeAPIView.as_view()),
    # path('cart/', views.CartViewSet.as_view({'post':'create'})),
    path('product/products/<int:pk>', views.ProductViewSet.as_view({'get':'retrieve'})),
    path('product/products/', views.ProductPaginatedViewSet.as_view()),
    # path('', views.ProductPaginatedViewSet.as_view()),
]