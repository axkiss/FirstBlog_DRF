from django.core.mail import BadHeaderError
from rest_framework import viewsets, permissions, pagination
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from taggit.models import Tag

from blog_project_drf.settings import EMAIL_FEEDBACK
from .serializers import PostSerializer, TagCloudSerializer, PopularPostSerializer, FeedBackSerializer
from .models import Post
from .services import get_popular_posts
from .utils import send_feedback


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


class TagCloudListView(ListAPIView):
    """Sorted list of tags with amount of their use"""
    serializer_class = TagCloudSerializer
    queryset = Post.tag.most_common()
    permission_classes = [permissions.AllowAny]


class PopularPostListView(ListAPIView):
    """List of popular posts for n days"""
    serializer_class = PopularPostSerializer
    queryset = get_popular_posts(Post, days=7, cnt_posts=5)
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    """Sending feedback from the blog to EMAIL_FEEDBACK"""
    permission_classes = [permissions.AllowAny]
    serializer_class = FeedBackSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                send_feedback(request, serializer.validated_data, EMAIL_FEEDBACK)
            except BadHeaderError as error:
                return Response({"status": error})
            return Response({"status": "success"})
        return Response({"status": "invalid data"})


