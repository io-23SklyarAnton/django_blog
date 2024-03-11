from django import template
from django.template.defaultfilters import stringfilter
from autocorrect import Speller
from django.db.models import Count

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def autocorrect(value):
    spell = Speller()
    return spell(value)


@register.inclusion_tag('blog/includes/recent-posts.html')
def recent_posts(value=3):
    from ..models import Post
    posts = Post.published.order_by('-publish')[:value]
    return {'posts': posts}


@register.inclusion_tag('blog/includes/popular-posts.html')
def popular_posts(value=3):
    from ..models import Post
    posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:value]
    return {'posts': posts}
