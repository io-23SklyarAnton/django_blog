from django.shortcuts import render, get_object_or_404
from .models import Post


def all_post_list(request):
    posts = Post.published.all()

    return render(request, 'post-list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    return render(request, 'post-detail.html', {'post': post})
