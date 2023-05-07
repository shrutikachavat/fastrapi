from django.urls import path
# from django.urls import include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()


urlpatterns = [
    # product
    path('product/products/<int:pk>', views.ProductViewSet.as_view({'get':'retrieve'})),
]