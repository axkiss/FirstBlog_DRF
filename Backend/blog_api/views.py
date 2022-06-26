from rest_framework import viewsets, permissions, pagination

from .serializers import PostSerializer
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

