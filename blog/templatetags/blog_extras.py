from django import template
from django.template.defaultfilters import stringfilter
from autocorrect import Speller

from blog.services.redis_services import get_redis_dispatcher

register = template.Library()

r = get_redis_dispatcher()


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
    posts_rank = r.zrange("total_views", 0, -1, desc=True)
    posts_rank_ids = [int(p_id) for p_id in posts_rank][:value]
    posts = list(Post.published.filter(id__in=posts_rank_ids))
    posts.sort(key=lambda x: posts_rank_ids.index(x.id))
    return {'posts': posts}
