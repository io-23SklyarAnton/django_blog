from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView

from .models import Post, Comment
from .forms import EmailForm, PostForm, CommentForm


def home_page(request):
    return render(request, 'blog/home_page.html')


class AllPostList(ListView):
    template_name = 'blog/post/post-list.html'
    paginate_by = 2
    queryset = Post.published.all()
    context_object_name = 'posts'


class PostDetail(DetailView, FormView, LoginRequiredMixin):
    queryset = Post.published.all()
    template_name = 'blog/post/post-detail.html'
    slug_url_kwarg = 'post_slug'
    form_class = CommentForm
    success_url = '#'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            return self.handle_no_permission()
        post = self.get_object()
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.mail = self.request.user.email
        comment.save()
        return super().form_valid(form)


class SharePost(LoginRequiredMixin, FormView):
    template_name = "blog/post/share-post.html"
    form_class = EmailForm
    success_url = "post/share-post.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'], slug=self.kwargs['post_slug'])
        form.send_mail(self.request, post)
        return render(self.request, 'blog/post/share-post.html', {'post': post, 'form': EmailForm(), 'sent': True})


class PostCreate(LoginRequiredMixin, FormView):
    template_name = 'blog/post/post-create.html'
    form_class = PostForm
    success_url = 'post/post-create.html'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'blog/post/post-create.html', {'form': form, 'sent': True})
