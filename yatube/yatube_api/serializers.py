from rest_framework import serializers
from posts.models import Post, Comments  # noqa


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов"""

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'group', 'image',)


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""

    class Meta:
        model = Comments
        fields = ('id', 'post', 'author', 'text', 'created',)
