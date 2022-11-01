from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Topic(models.Model):
    """ Модель темы """
    title = models.CharField(max_length=255)
    total_comments = models.IntegerField()

    def __str__(self):
        return self.title

    def total_posts(self):
        """ Get every post in this topic """
        return Post.objects.filter(topic=self).count()

    def counted_total_comments(self):
        return self.total_comments

    def last_post(self):
        return Post.objects.filter(topic=self).last()

    def get_absolute_url(self):
        return reverse('forum:topic', kwargs={'topic_id': self.pk})

    def get_posts(self):
        return Post.objects.filter(topic=self).order_by('-date')


class Comment(models.Model):
    """ Comment on post model """
    author = models.ForeignKey("shop.Customer", on_delete=models.CASCADE, related_name='commentAuthor')
    post = models.ForeignKey("forum.Post", on_delete=models.CASCADE, related_name='commentPost')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('shop.Customer', related_name='customer_comment_likes')
    dislikes = models.ManyToManyField('shop.Customer', related_name='customer_comment_dislikes')
    content = HTMLField()

    def __str__(self):
        return self.author, self.post.name[:25]

    def count_likes(self):
        return self.likes.count()

    def count_dislikes(self):
        return self.dislikes.count()


class Ip(models.Model):
    ip = models.CharField(max_length=255)

    def __str__(self):
        return self.ip


class Post(models.Model):
    """ Post model """
    name = models.CharField(max_length=200)
    content = HTMLField()
    author = models.ForeignKey("shop.Customer", on_delete=models.CASCADE, related_name="postAuthor")
    date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topic")
    closed = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    views = models.ManyToManyField('forum.Ip', related_name='views', blank=True)
    likes = models.ManyToManyField('shop.Customer', related_name='customer_likes')
    dislikes = models.ManyToManyField('shop.Customer', related_name='customer_dislikes')

    def __str__(self):
        return self.name

    def count_comments(self):
        return Comment.objects.filter(post=self).count()

    def latest_comment(self):
        return Comment.objects.filter(post=self).order_by('-date').first()

    def get_absolute_url(self):
        return reverse('forum:post_detail', kwargs={'post_id': self.pk})

    def get_comments(self):
        return Comment.objects.filter(post=self).order_by('-date')

    def count_likes(self):
        return self.likes.count()

    def count_dislikes(self):
        return self.dislikes.count()

    def get_views(self):
        return self.views.count()