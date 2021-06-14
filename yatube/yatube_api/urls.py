from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


from .views import PostViewsSet, CommentsViewsSet


router = DefaultRouter()
router.register('posts', PostViewsSet, basename="api_posts")
router.register(r'posts/(?P<post_id>[0-9]+)/comments', CommentsViewsSet, basename="api_comments")


urlpatterns = [
    path('token-auth/', views.obtain_auth_token, name="api_login"),  # авторизация (получение токена)
    path('', include(router.urls)),
]
