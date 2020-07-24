from django.urls import path, include
from rest_framework import routers

from photos.views import PhotoViewSet

router = routers.DefaultRouter()
router.register(r'photos', PhotoViewSet)

app_name = 'api_v1'

urlpatterns = [
    path('', include(router.urls)),
]
