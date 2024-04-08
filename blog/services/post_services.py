from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.db.models import QuerySet, Count
from django.shortcuts import get_object_or_404

from blog.forms import CommentForm, EmailForm, PostForm, SearchForm
from blog.models import Post

import redis

from blog_project import settings

r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)


def get_posts_by_tag_or_search_query(request: WSGIRequest, tag: str, is_published: bool = True) -> QuerySet:
    """returns query of posts filtered by the tag nor search expression"""
    query = request.GET.get('query')
    results = Post.published.all() if is_published else Post.objects.all()
    if tag:
        results = results.filter(tags__name__in=[tag])
    if query:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('text', weight='B')
            search_query = SearchQuery(query)
            results = results.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(
                search=search_query, rank__gte=0.2).order_by('-rank')
        return results
    return results


def get_similar_posts(post: Post) -> QuerySet:
    """counts the amount of tag matches of a specific and all posts
    then returns a query of a similar posts based on it"""
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(num_tags=Count('tags')).order_by('-num_tags', '-publish')[:4]
    return similar_posts


def add_comment_to_post(request: WSGIRequest, post: Post, form: CommentForm) -> None:
    """creates a comment object in the Comment model"""
    comment = form.save(commit=False)
    comment.post = post
    comment.author = request.user
    comment.mail = request.user.email
    comment.save()


def send_email(form: EmailForm, request: WSGIRequest, **kwargs) -> None:
    """sends a letter to share the post via an email"""
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             pk=kwargs['pk'],
                             slug=kwargs['slug'])

    post_url = request.build_absolute_uri(post.get_absolute_url())
    title = f"{form.cleaned_data['name']} wants you to read {post.title}"
    description = f"he sent you this message: {form.cleaned_data['description']}. Watch it on {post_url}"
    send_mail(title, description, '80kap.i.toshka@gmail.com', [form.cleaned_data['to']])


def create_post(form: PostForm, request: WSGIRequest) -> None:
    """creates a post object in Post the model"""
    obj = form.save(commit=False)
    obj.author = request.user
    obj.save()
    form.save_m2m()


def get_all_tag_names_from_kwargs(**kwargs) -> list:
    """returns list of tag names"""
    return list(kwargs.values())


def get_post_instance(pk: int) -> Post:
    """returns curtain post or 404 Error if not found"""
    return get_object_or_404(Post, pk=pk)


def get_all_published_posts() -> QuerySet:
    """returns all published posts"""
    return Post.published.all()


def get_all_posts() -> QuerySet:
    """returns all posts"""
    return Post.objects.all()


def get_all_user_posts(author: User, queryset: QuerySet = None) -> QuerySet:
    """returns all posts from a certain user
    takes optional param queryset to filter certain query
    """
    result = queryset or Post.objects.all()
    return result.filter(author=author)


def increase_views(post_name):
    """increase the num of views in the redis storage"""
    return r.incr(post_name)


def get_var(var_name):
    """return a variable from the redis storage"""
    return r.get(var_name)
