from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('tag/<str:tag>/', views.AllPostList.as_view(), name='posts_by_tag'),
    path('', views.AllPostList.as_view(), name='all_posts'),
    path('my_posts/<str:username>', views.UserPosts.as_view(), name='user_posts'),
    path('share_post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.SharePost.as_view(),
         name='share_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.PostDetail.as_view(),
         name='post_detail'),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
]
