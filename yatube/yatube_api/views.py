from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, User  # noqa
from .serializers import PostSerializer
from rest_framework import status


class PostViewsSet(ModelViewSet):
    """Класс CRUD для постов для API"""

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        """Вывод всех постов"""

        queryset = self.queryset.order_by('-pub_date').all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):  # noqa
        """Изменение существующего поста"""

        post = self.queryset.get(pk=pk)
        serializer = self.serializer_class(post, data=request.data)
        if post.author == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):  # noqa
        """Удаление поста"""

        post = self.queryset.get(pk=pk)
        serializer = self.serializer_class(post)
        if post.author == request.user:
            post.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)

    def create(self, request):  # noqa
        """Создание поста"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
