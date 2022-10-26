from celery import shared_task
from .models import Topic, Post, Comment


@shared_task()
def count_topic_total_messages():
    for topic in Topic.objects.all():
        topic.total_comments = Comment.objects.filter(post__topic=topic).count()
        topic.save()

