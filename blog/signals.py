from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from blog.models import Post
from blog.services.redis_services import get_redis_dispatcher


@receiver(post_delete, sender=Post)
def post_delete_from_redis(sender, instance, **kwargs):
    r = get_redis_dispatcher()
    r.delete(f"post:{instance.id}:views")
    r.zrem("total_views", f"{instance.id}")
