from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


from .views import PostViewsSet


router = DefaultRouter()
router.register('posts', PostViewsSet, basename="api_posts")

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),  # авторизация (получение токена)
    path('', include(router.urls)),
    # path('posts/add/', api_post_add, name='api_post_add'),
    # path('posts/edit/', api_post_edit, name='api_post_edit'),
    # path('posts/delete/', api_post_del, name='api_post_delete')
]
