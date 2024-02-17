from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class AllPostList(ListView):
    template_name = 'post/post-list.html'
    paginate_by = 2
    queryset = Post.published.all()
    context_object_name = 'posts'


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                             publish__day=day, slug=post_slug)

    return render(request, 'post/post-detail.html', {'post': post})
