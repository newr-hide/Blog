from django.contrib import admin
from .models import Post, Comment


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date_published']

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)


class CommentPostAdmin(admin.ModelAdmin):
    list_comment_display = ['id', 'post', 'date_published']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentPostAdmin)
