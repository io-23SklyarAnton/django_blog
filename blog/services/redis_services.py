import redis
from blog_project import settings


def get_redis_dispatcher():
    return redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)


r = get_redis_dispatcher()


def increase_views(post_id: int):
    """increase the num of views in the redis storage"""
    r.zincrby("total_views", 1, f"{post_id}")
    return r.incr(f"post:{post_id}:views")


def get_var(var_name):
    """return a variable from the redis storage"""
    return r.get(var_name)
