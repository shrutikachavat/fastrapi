from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()


urlpatterns = [
    path('', views.HomeAPIView.as_view()),
    path('item/items/<int:pk>', views.ItemViewSet.as_view({'get':'retrieve'})),
    path('item/items/', views.ItemPaginatedViewSet.as_view()),
    # path('', views.ItemPaginatedViewSet.as_view()),
]