from rest_framework import viewsets, permissions, pagination
from rest_framework.generics import get_object_or_404, ListAPIView

from taggit.models import Tag

from .serializers import PostSerializer, TagSerializer
from .models import Post


class MyPageNumberPagination(pagination.PageNumberPagination):
    """Default pagination"""
    page_size = 20
    page_size_query_param = 'page_size'


class PostViewSet(viewsets.ModelViewSet):
    """List of posts and detail"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = MyPageNumberPagination


class TagListView(ListAPIView):
    """List of posts including tag"""
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag).order_by('-id')
        return posts


class TagsCloudListView(ListAPIView):
    """List of all tags"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.AllowAny]
