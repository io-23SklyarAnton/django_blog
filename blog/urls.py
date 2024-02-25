from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [path('', views.AllPostList.as_view(), name='all_posts'),
               path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.PostDetail.as_view(),
                    name='post_detail'),
               path('create_post/', views.PostCreate.as_view(), name='create_post'),
               ]
