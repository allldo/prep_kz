from django.shortcuts import render, get_object_or_404

from shop.service import get_customer
from .models import Post, Comment, Topic
from shop.models import Customer


def main_forum(request):
    context = {'latest_comment': Comment.objects.all().order_by('-date')[:3],
               'total_posts': Post.objects.all().count(),
               'total_comments': Comment.objects.all().count(),
               'total_users': Customer.objects.all().count(),
               'topics': Topic.objects.all(),
               'customer': get_customer(request)}
    # total users добавить флаг у кастомера на активность на форуме
    return render(request, 'forum/forum_main.html', context)


def topic(request, topic_id):
    context = {
        'topic': get_object_or_404(Topic, pk=topic_id)
    }
    return render(request, 'forum/topic_page.html', context)


def create_topic(request, topic_name):
    get_object_or_404(Topic, title=topic_name)
    context = {}
    return render(request, 'forum/create_topic.html', context)
