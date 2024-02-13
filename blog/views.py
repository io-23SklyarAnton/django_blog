from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def all_post_list(request):
    all_posts = Post.published.all()
    paginator = Paginator(all_posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post/post-list.html', {'posts': posts})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                             publish__day=day, slug=post_slug)

    return render(request, 'post/post-detail.html', {'post': post})
