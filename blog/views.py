from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .models import Post
from .forms import EmailForm, PostForm


def home_page(request):
    return render(request, 'home_page.html')


class AllPostList(ListView):
    template_name = 'post/post-list.html'
    paginate_by = 2
    queryset = Post.published.all()
    context_object_name = 'posts'


class PostDetail(View):
    def get(self, request, year, month, day, post_slug):
        post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                                 publish__day=day, slug=post_slug)
        return render(request, 'post/post-detail.html', {'post': post, 'form': EmailForm()})


class SharePost(View):
    def get(self, request, year, month, day, post_slug):
        return render(request, 'post/share-post.html', {'form': EmailForm()})

    def post(self, request, year, month, day, post_slug):
        post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                                 publish__day=day, slug=post_slug)
        form = EmailForm(request.POST)
        sent = False
        if form.is_valid():
            form.send_mail(request, post)
            sent = True
        return render(request, 'post/share-post.html', {'post': post, 'form': EmailForm(), 'sent': sent})


class PostCreate(View):
    form = PostForm()

    def get(self, request):
        return render(request, 'post/post-create.html', {'form': self.form})

    def post(self, request):
        sent = False
        form = PostForm(request.POST)
        if form.is_valid():
            sent = True
            form.save()
        return render(request, 'post/post-create.html', {'form': self.form, 'sent': sent})


@require_POST
def comment_post(request):
    pass
