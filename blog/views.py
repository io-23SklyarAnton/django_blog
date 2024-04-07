from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.contrib import messages

from .forms import EmailForm, PostForm, CommentForm, SearchForm
from blog.services.post_services import get_posts_by_tag_or_search_query, get_similar_posts, add_comment_to_post, \
    send_email, \
    create_post, \
    get_all_published_posts, get_all_user_posts, get_all_posts
from .models import Post


def home_page(request):
    return render(request, 'blog/home_page.html')


class AllPostList(ListView):
    """Shows post feed from all users"""
    template_name = 'blog/post/post-list.html'
    paginate_by = 2
    context_object_name = 'posts'

    def get_queryset(self):
        return get_posts_by_tag_or_search_query(self.request, self.kwargs.get('tag'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['tag'] = self.kwargs.get('tag')
        context['query'] = self.request.GET.get('query')
        context['search_form'] = SearchForm()
        return context


class UserPosts(LoginRequiredMixin, AllPostList):
    """Shows all posts by loginned user"""
    template_name = 'blog/post/user-posts.html'

    def get_queryset(self):
        """getting posts by current loginned user"""
        query = get_posts_by_tag_or_search_query(self.request, self.kwargs.get('tag'), is_published=False)
        return get_all_user_posts(author=self.request.user, queryset=query)


class PostDetail(DetailView, FormView, LoginRequiredMixin):
    """Shows the full post with comments and possibility to share this post"""
    queryset = get_all_published_posts()
    template_name = 'blog/post/post-detail.html'
    form_class = CommentForm
    success_url = '#'

    def get_context_data(self, **kwargs):
        """returns a list of the similar posts"""
        context = super().get_context_data(**kwargs)
        similar_posts = get_similar_posts(self.get_object())
        context['comment_form'] = CommentForm()
        context['similar_posts'] = similar_posts
        return context

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            return self.handle_no_permission()
        add_comment_to_post(request=self.request, post=self.get_object(), form=form)
        messages.success(self.request, message='comment added successfully !')
        return super().form_valid(form)


class UserPostDetail(PostDetail):
    """Shows the full user's post, but with possibility to edit this post"""
    template_name = 'blog/post/user-post-detail.html'
    queryset = get_all_posts()


class SharePost(LoginRequiredMixin, FormView):
    """Provide a share form to send a certain post via an email"""
    template_name = "blog/post/share-post.html"
    form_class = EmailForm
    success_url = "post/share-post.html"

    def form_valid(self, form):
        send_email(form, self.request, **self.kwargs)
        context = {'form': EmailForm()}
        messages.success(self.request, message='Email has sent successfully !')
        return render(self.request, 'blog/post/share-post.html', context)


class PostCreate(LoginRequiredMixin, FormView):
    """Provide a form to create a new post"""
    template_name = 'blog/post/post-create.html'
    form_class = PostForm

    def form_valid(self, form):
        create_post(form, self.request)
        messages.success(self.request, message='Post created successfully !')
        return render(self.request, 'blog/post/post-create.html', {'form': form})

    def get_success_url(self):
        return reverse_lazy('blog:user_posts', kwargs={'username': self.request.user.get_username()})


class PostEdit(UpdateView):
    """Provide a form to change your post"""
    template_name = 'blog/post/post-edit.html'
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.success(self.request, message='post edited successfully')
        return reverse_lazy('blog:user_post_detail', kwargs=self.kwargs)
