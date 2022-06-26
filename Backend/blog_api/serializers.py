from rest_framework import serializers

from taggit.models import Tag
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from users_api.models import User
from .models import Post


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
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
