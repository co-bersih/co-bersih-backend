from rest_framework import serializers
from .models import Blog
from apps.user.serializers import UserSerializer


class BlogSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    image_url = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)
    published_date = serializers.ReadOnlyField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'image', 'image_url', 'author', 'published_date', 'content']