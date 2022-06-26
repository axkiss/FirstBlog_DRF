from django.contrib import admin
from .models import Post


class AuthorFilter(admin.SimpleListFilter):
    """
    Filter show only the authors who wrote the post
    """
    title = 'Authors'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = Post.objects.order_by().values('author_id', 'author__username').distinct()
        return [tuple(author.values()) for author in authors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ('views',)
    list_display = ('title', 'author', 'post_tags', 'views', 'created_at', 'edited_at',)
    list_per_page = 25
    list_filter = (AuthorFilter, 'tag',)
    ordering = ('created_at', 'edited_at', 'views')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='TAGS')
    def post_tags(self, obj):
        return list(obj.tag.names())