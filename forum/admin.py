from django.contrib import admin
from .models import Comment, Topic, Post, Ip


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Topic)
admin.site.register(Ip)
admin.site.register(Post, PostAdmin)
