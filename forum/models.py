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
        """ Get total number of comments in topic """
        return self.total_comments

    def last_post(self):
        """ Get last post published in topic """
        return Post.objects.filter(topic=self).last()

    def get_absolute_url(self):
        """ Get absolute url for template usage """
        return reverse('forum:topic', kwargs={'topic_id': self.pk})

    def get_posts(self):
        """ Get all posts in topic """
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
        return str(self.author) + self.post.name[:25]

    def count_likes(self):
        """ Get integer number of likes on comment """
        return self.likes.count()

    def count_dislikes(self):
        """ Get integer number of dislikes on comment """
        return self.dislikes.count()


class Ip(models.Model):
    """ Model for counting views on posts """
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
        """ Count comments on post """
        return Comment.objects.filter(post=self).count()

    def latest_comment(self):
        """ Get latest comment on post """
        return Comment.objects.filter(post=self).order_by('-date').first()

    def get_absolute_url(self):
        """ Get url for template usage """
        return reverse('forum:post_detail', kwargs={'post_id': self.pk})

    def get_comments(self):
        """ Get all comments on post """
        return Comment.objects.filter(post=self).order_by('-date')

    def count_likes(self):
        """ Get integer number of likes on post """
        return self.likes.count()

    def count_dislikes(self):
        """ Get integer number of dislikes on post """
        return self.dislikes.count()

    def get_views(self):
        """ Get integer number of views on post """
        return self.views.count()


class Report(models.Model):
    """ Report model """
    report_body = models.CharField(max_length=600)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='post_report')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='comment_report')
    from_user = models.ForeignKey('shop.Customer', on_delete=models.CASCADE, related_name='report_author')

    def __str__(self):
        return self.report_body
