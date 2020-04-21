from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from blog.models import Post
from .serializer import PostSerializer


class PostViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  CreateModelMixin, DestroyModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, pk, format=None):
        post = get_object_or_404(self.queryset, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


