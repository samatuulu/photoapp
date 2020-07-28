from django.urls import path, include
from rest_framework import routers

from photos.views import PhotoViewSet, TagListView, PhotoCreateAPIView

router = routers.DefaultRouter()
router.register(r'photos', PhotoViewSet, basename='photos')

app_name = 'api_v1'

urlpatterns = [
    path('', include(router.urls)),
    path('hashtag/<int:pk>/', TagListView.as_view()),
    path('add/photos/', PhotoCreateAPIView.as_view())
]
