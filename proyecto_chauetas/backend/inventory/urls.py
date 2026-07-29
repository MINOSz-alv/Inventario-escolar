from rest_framework import routers
from .views import ItemViewSet, CategoryViewSet, LocationViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'locations', LocationViewSet, basename='location')

urlpatterns = [
    path('', include(router.urls)),
]
