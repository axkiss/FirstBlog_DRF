from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('tags', views.TagCloudListView.as_view(), name='tags'),
    path('tags/<slug:slug>', views.TagListView.as_view(), name='tag'),
    path('popular_posts', views.PopularPostListView.as_view(), name='popular_posts'),
    path('feedback', views.FeedBackView.as_view(), name='feedback'),
    path('search/', views.SearchPostListView.as_view(), name='search'),
    path('comments/<slug:post_slug>', views.CommentListView.as_view(), name='post_comments'),
    path('comments/<slug:post_slug>/add/', views.AddCommentView.as_view(), name='add_comment')

]