from rest_framework import serializers

from taggit.models import Tag
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from users_api.models import User
from .models import Post, Comment


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags in posts"""

    class Meta:
        model = Tag
        fields = ('name', 'slug')


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for model Post (list and retrieve actions)"""
    tag = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'


class CreateUpdatePostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for model Post (create and update actions)"""
    tag = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'author', 'tag')


class TagCloudSerializer(serializers.Serializer):
    """Serializer for tag cloud (list of all tags)"""
    name = serializers.CharField()
    slug = serializers.CharField()
    num_times = serializers.IntegerField()


class PopularPostSerializer(serializers.ModelSerializer):
    """Serializer for the most popular posts on blog"""

    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'slug')


class FeedBackSerializer(serializers.Serializer):
    """Serializer for Feedback message"""
    name = serializers.CharField(min_length=2, max_length=256)
    email_from = serializers.EmailField()
    subject = serializers.CharField(min_length=2, max_length=256)
    main_body = serializers.CharField(min_length=2)


class SearchPostSerializer(serializers.ModelSerializer):
    """Serializer for posts in search results"""

    class Meta:
        model = Post
        fields = ('title', 'description', 'thumbnail', 'slug')


class CommentListSerializer(serializers.ModelSerializer):
    """Serializer for list comments of post"""
    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field="slug", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "username", "text", "created_at")


class AddCommentSerializer(serializers.ModelSerializer):
    """Serializer for create comment to post"""

    class Meta:
        model = Comment
        fields = ('text',)
