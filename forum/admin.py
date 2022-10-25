from django.contrib import admin
from .models import Tag, Topic, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date')


admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(Post, PostAdmin)
