import re
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics

from photos.models import Photo, Tag
from photos.serializers import PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

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
        return Response({serializer.errors, status.HTTP_400_BAD_REQUEST})


class TagListView(generics.ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        hashtag_id = get_object_or_404(Tag, pk=self.kwargs['pk'])
        caption = Photo.objects.filter(caption__icontains=hashtag_id)
        return caption
