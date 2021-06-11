from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Post # noqa
from .serializers import PostSerializer
from rest_framework import status


@api_view(['GET'])
def api_post_views(requests):
    if requests.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'PUT'])
def api_post_add(requests):
    if requests.method == "POST":
        serializer = PostSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'PUT'])
def api_post_edit(requests):
        if requests.method == 'PATCH' or requests.method == 'PUT':
            post = Post.objects.get(pk=requests.data['id'])
            serializer = PostSerializer(post, data=requests.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def api_post_del(requests):
    if requests.method == "DELETE":
        post = Post.objects.get(pk=requests.data['id'])
        post.delete()
        return Response({'message': 'post delete'}, status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
