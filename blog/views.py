from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from .forms import EmailForm, PostForm, CommentForm
from blog.services.post_services import get_posts_by_tag, get_similar_posts, add_comment_to_post, send_email, \
    create_post, \
    get_post_instance, get_all_published_posts


def home_page(request):
    return render(request, 'blog/home_page.html')


class AllPostList(ListView):
    """Shows post feed from all users"""
    template_name = 'blog/post/post-list.html'
    paginate_by = 2
    context_object_name = 'posts'

    def get_queryset(self):
        return get_posts_by_tag(self.kwargs.get('tag'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['tag'] = self.kwargs.get('tag')
        return context


class UserPosts(LoginRequiredMixin, ListView):
    """Shows all posts by loginned user"""
    template_name = 'blog/post/user-posts.html'
    paginate_by = 2
    context_object_name = 'posts'

    def get_queryset(self):
        return get_all_published_posts().filter(author=self.request.user)


class PostDetail(DetailView, FormView, LoginRequiredMixin):
    """Shows the full post with comments and possibility to share this post"""
    queryset = get_all_published_posts()
    template_name = 'blog/post/post-detail.html'
    form_class = CommentForm
    success_url = '#'

    def get_context_data(self, **kwargs):
        """returns a list of the similar posts"""
        context = super().get_context_data(**kwargs)
        return get_similar_posts(self.get_object(), context)

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            return self.handle_no_permission()
        add_comment_to_post(request=self.request, post=self.get_object(), form=form)
        return super().form_valid(form)


class UserPostDetail(PostDetail):
    """Shows the full user's post, but with possibility to edit this post"""
    template_name = 'blog/post/user-post-detail.html'


class SharePost(LoginRequiredMixin, FormView):
    """Provide a share form to send a certain post via an email"""
    template_name = "blog/post/share-post.html"
    form_class = EmailForm
    success_url = "post/share-post.html"

    def form_valid(self, form):
        send_email(form, self.request, **self.kwargs)
        context = {'form': EmailForm(), 'sent': True}
        return render(self.request, 'blog/post/share-post.html', context)


class PostCreate(LoginRequiredMixin, FormView):
    """Provide a form to create a new post"""
    template_name = 'blog/post/post-create.html'
    form_class = PostForm
    success_url = 'post/post-create.html'

    def form_valid(self, form):
        create_post(form, self.request)
        return render(self.request, 'blog/post/post-create.html', {'form': form, 'sent': True})


class PostEdit(PostCreate):
    """Provide a form to change your post"""
    template_name = 'blog/post/post-edit.html'

    def get_form_kwargs(self):
        """adds Post instance arg to form"""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_post_instance(self.kwargs.get('pk'))
        return kwargs

    def get_success_url(self):
        return reverse_lazy('blog:user_posts', kwargs={'username': self.request.user.get_username()})
