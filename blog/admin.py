from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'tags', 'author', 'publish', 'status']
    list_filter = ['status', 'publish', 'author', 'tags']
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tags(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
