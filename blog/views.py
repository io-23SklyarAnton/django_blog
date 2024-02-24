from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail

from .models import Post
from .forms import EmailForm


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

    def post(self, request, year, month, day, post_slug):
        post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                                 publish__day=day, slug=post_slug)
        form = EmailForm(request.POST)
        sent = False
        if form.is_valid():
            clear_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            title = f"{clear_data['name']} wants you to read {post.title}"
            description = f"he sent you this message: {clear_data['description']}. Watch it on {post_url}"
            send_mail(title, description, '80kap.i.toshka@gmail.com', [clear_data['to']])
            sent = True
        return render(request, 'post/post-detail.html', {'post': post, 'form': EmailForm(), 'sent': sent})
