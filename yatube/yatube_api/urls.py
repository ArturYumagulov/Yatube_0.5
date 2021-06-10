from django.urls import path
from rest_framework.authtoken import views


from .views import api_post_views, api_post_add, api_post_edit, api_post_del

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),  # авторизация
    path('posts/', api_post_views, name='api_posts'),
    path('posts/add/', api_post_add, name='api_post_add'),
    path('posts/edit/', api_post_edit, name='api_post_edit'),
    path('posts/delete/', api_post_del, name='api_post_delete')
]
