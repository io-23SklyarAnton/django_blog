from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
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


class PostDetail(DetailView):
    queryset = Post.published.all()
    template_name = 'post/post-detail.html'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmailForm()
        return context


class SharePost(FormView):
    template_name = "post/share-post.html"
    form_class = EmailForm
    success_url = "post/share-post.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'], slug=self.kwargs['post_slug'])
        form.send_mail(self.request, post)
        return render(self.request, 'post/share-post.html', {'post': post, 'form': EmailForm(), 'sent': True})


class PostCreate(FormView):
    template_name = 'post/post-create.html'
    form_class = PostForm
    success_url = 'post/post-create.html'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'post/post-create.html', {'form': form, 'sent': True})


@require_POST
def comment_post(request):
    pass
