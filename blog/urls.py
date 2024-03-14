from django.urls import path
from . import views
import os

app_name = 'blog'
concrete_post_url = '<int:pk>/<slug:post_slug>/'

urlpatterns = [
    path('tag/<str:tag>/', views.AllPostList.as_view(), name='posts_by_tag'),
    path('', views.AllPostList.as_view(), name='all_posts'),
    path('my_posts/<str:username>', views.UserPosts.as_view(), name='user_posts'),
    path(os.path.join('share_post/', concrete_post_url), views.SharePost.as_view(),
         name='share_post'),
    path(os.path.join('user_post/', concrete_post_url), views.UserPostDetail.as_view(), name='user_post_detail'),
    path(concrete_post_url, views.PostDetail.as_view(), name='post_detail'),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    path(os.path.join('edit_post/', concrete_post_url), views.PostEdit.as_view(), name='edit_post')
]
