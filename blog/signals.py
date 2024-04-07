from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Post


@receiver(post_save, sender=Post)
def successfully_saved_message(sender, **kwargs):
    print('Post saved')
