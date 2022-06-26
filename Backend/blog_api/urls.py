from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('tags', views.TagsCloudListView.as_view(), name='tags'),
    path('tags/<slug:slug>', views.TagListView.as_view(), name='tag'),

]