from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView

from .models import Post
from .forms import EmailForm, PostForm, CommentForm
from .post_services import get_posts_by_tag, get_similar_posts, add_comment_to_post, send_email, create_post


def home_page(request):
    return render(request, 'blog/home_page.html')


class AllPostList(ListView):
    """Shows post feed"""
    template_name = 'blog/post/post-list.html'
    paginate_by = 2
    context_object_name = 'posts'

    def get_queryset(self):
        return get_posts_by_tag(self.kwargs.get('tag'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['tag'] = self.kwargs.get('tag')
        return context


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
        return get_similar_posts(self.get_object(), context)

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            self.handle_no_permission()
        add_comment_to_post(request=self.request, post=self.get_object(), form=form)
        return super().form_valid(form)


class SharePost(LoginRequiredMixin, FormView):
    template_name = "blog/post/share-post.html"
    form_class = EmailForm
    success_url = "post/share-post.html"

    def form_valid(self, form):
        send_email(form, self.request, **self.kwargs)
        context = {'form': EmailForm(), 'sent': True}
        return render(self.request, 'blog/post/share-post.html', context)


class PostCreate(FormView):
    template_name = 'blog/post/post-create.html'
    form_class = PostForm
    success_url = 'post/post-create.html'

    def form_valid(self, form):
        create_post(form, self.request)
        return render(self.request, 'blog/post/post-create.html', {'form': form, 'sent': True})


class UserPosts(LoginRequiredMixin, ListView):
    template_name = 'blog/post/user-posts.html'
    paginate_by = 2
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.published.all().filter(author=self.request.user)
