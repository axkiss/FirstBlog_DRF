from rest_framework import serializers

from taggit.models import Tag
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from users_api.models import User
from .models import Post


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags in posts"""

    class Meta:
        model = Tag
        fields = ('name', 'slug')


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for model Post"""
    tag = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'


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
