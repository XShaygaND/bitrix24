from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DealViewset


router = DefaultRouter()
router.register(r'handler', DealViewset, basename='handler')

urlpatterns = [
    path('', include(router.urls)),
]
