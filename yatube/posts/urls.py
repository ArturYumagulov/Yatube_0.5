from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("group/<slug>/", views.group_posts, name="group"),
    path('new/', views.new_post, name='new_post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/<int:post_id>/', views.post_views, name='post_view'),
    path('profile/<str:username>/<int:post_id>/edit/', views.post_edit, name="edit_post"),
    path("profile/<username>/<int:post_id>/comment", views.add_comment, name="add_comment"),
]
