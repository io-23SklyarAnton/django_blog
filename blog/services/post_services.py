from django.core.mail import send_mail
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from blog.forms import CommentForm, EmailForm, PostForm
from blog.models import Post


def get_posts_by_tag(tag: str) -> QuerySet:
    if tag:
        return Post.published.filter(tags__name__in=[tag])
    return Post.published.all()


def get_similar_posts(post: Post, context: dict) -> dict:
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(num_tags=Count('tags')).order_by('-num_tags', '-publish')[:4]
    context['comment_form'] = CommentForm()
    context['similar_posts'] = similar_posts
    return context


def add_comment_to_post(request: HttpRequest, post: Post, form: CommentForm) -> None:
    comment = form.save(commit=False)
    comment.post = post
    comment.author = request.user
    comment.mail = request.user.email
    comment.save()


def send_email(form: EmailForm, request: HttpRequest, **kwargs) -> None:
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             pk=kwargs['pk'],
                             slug=kwargs['post_slug'])

    post_url = request.build_absolute_uri(post.get_absolute_url())
    title = f"{form.cleaned_data['name']} wants you to read {post.title}"
    description = f"he sent you this message: {form.cleaned_data['description']}. Watch it on {post_url}"
    send_mail(title, description, '80kap.i.toshka@gmail.com', [form.cleaned_data['to']])


def create_post(form: PostForm, request: HttpRequest) -> None:
    obj = form.save(commit=False)
    obj.author = request.user
    obj.save()
    form.save_m2m()


def get_all_tag_names_from_kwargs(**kwargs) -> list:
    return list(kwargs.values())


def get_post_instance(pk: int) -> Post:
    return get_object_or_404(Post, pk=pk)


def get_all_published_posts() -> QuerySet:
    return Post.published.all()
