from django.core.mail import BadHeaderError
from rest_framework import viewsets, permissions, pagination
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from taggit.models import Tag

from blog_project_drf.settings import EMAIL_FEEDBACK
from .serializers import PostSerializer, TagCloudSerializer, PopularPostSerializer, FeedBackSerializer, \
    SearchPostSerializer, CommentListSerializer, AddCommentSerializer
from .models import Post, Comment
from .services import get_popular_posts, get_results_search
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


class CommentListCreateView(ListCreateAPIView):
    """List comments of post or create comment"""
    serializer_class = CommentListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug)
        return post.comments.all()

    def post(self, request, *args, **kwargs):
        serializer = AddCommentSerializer(data=request.data)
        if serializer.is_valid():
            post_slug = self.kwargs.get('post_slug')
            post = get_object_or_404(Post, slug=post_slug)
            text = serializer.validated_data['text']
            new_comment = Comment(post=post, username=request.user, text=text)
            new_comment.save()
            return Response({"detail": "Success"})
        return Response({"detail": "Invalid data"})


# class AddCommentView(APIView):
#     """Add comment to post"""
#     serializer_class = AddCommentSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             post_slug = self.kwargs.get('post_slug')
#             post = get_object_or_404(Post, slug=post_slug)
#             text = serializer.validated_data['text']
#             new_comment = Comment(post=post, username=request.user, text=text)
#             new_comment.save()
#             return Response({"detail": "Success"})
#         return Response({"detail": "Invalid data"})
#

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
    serializer_class = FeedBackSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                send_feedback(request, serializer.validated_data, EMAIL_FEEDBACK)
            except BadHeaderError as error:
                return Response({"status": error})
            return Response({"status": "success"})
        return Response({"status": "invalid data"})


class SearchPostListView(ListAPIView):
    """List of posts including a search query"""
    serializer_class = SearchPostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        return get_results_search(Post, search_query, posts_on_page=self.pagination_class.page_size)
