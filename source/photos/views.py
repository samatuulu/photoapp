import re
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, permissions

from source.photos.models import Photo, Tag
from source.photos.serializers import PhotoSerializer


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsOwner,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            instance = Photo.objects.get(id=serializer.data['id'])
            pattern = r"#\w+"
            tags = re.findall(pattern, instance.caption)
            if tags:
                tag_list = []
                for tag in tags:
                    obj, created = Tag.objects.get_or_create(name=tag)
                    tag_list.append(obj)
                instance.tags.set(tag_list)
            return Response(serializer.data)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Photo.objects.filter(author=user)
        return PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagListView(generics.ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        hashtag_id = get_object_or_404(Tag, pk=self.kwargs['pk'])
        caption = Photo.objects.filter(caption__icontains=hashtag_id)
        return caption


class PhotoCreateAPIView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsOwner,)

    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        if serializers.is_valid():
            for photo in request.FILES.getlist('photo'):
                obj = Photo.objects.create(photo=photo, caption=serializers.data['caption'], author=self.request.user)
                serializers = PhotoSerializer(obj)
            return Response(serializers.data)
        return Response({'detail': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
