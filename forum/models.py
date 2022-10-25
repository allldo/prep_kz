from django.db import models
from tinymce.models import HTMLField


class Topic(models.Model):
    """ Модель темы """
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ Модель комментария """
    author = models.ForeignKey("shop.Customer", on_delete=models.CASCADE, related_name='commentAuthor')
    post = models.ForeignKey("forum.Post", on_delete=models.CASCADE, related_name='commentPost')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    content = HTMLField()


class Post(models.Model):
    """ Модель поста """
    name = models.CharField(max_length=200)
    content = HTMLField()
    author = models.ForeignKey("shop.Customer", on_delete=models.CASCADE, related_name="postAuthor")
    date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topic")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
