from django.contrib import admin
from .models import Comment, Topic, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date')


admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(Post, PostAdmin)
