from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from shop.service import get_customer
from .models import Post, Comment, Topic
from shop.models import Customer

from .services import like_or_dislike

from .forms import TinyForm


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


def create_post(request, topic_name):
    form = TinyForm()
    top_ic = get_object_or_404(Topic, title=topic_name)
    context = {
        'form': form,
        'topic': top_ic,
    }
    return render(request, 'forum/create_post.html', context)


@require_POST
def new_post(request, topic_name):
    top_ic = get_object_or_404(Topic, title=topic_name)
    post = Post.objects.create(topic=top_ic, author=get_customer(request),
                               name=request.POST.get('post_name'),
                               content=request.POST.get('content'))
    return HttpResponseRedirect(reverse('forum:post_detail', kwargs={
        'post_id': post.pk
    }))


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
        'topic': post.topic,
        'comments': post.get_comments,
    }
    return render(request, 'forum/post_detail.html', context)


@require_POST
def like(request, post_id):
    _, default = like_or_dislike(request, request.POST.get('comment_pk'), True)
    return JsonResponse({
        'liked': True, 'default': default
    })


@require_POST
def dislike(request, post_id):
    _, default = like_or_dislike(request, request.POST.get('comment_pk'), False)
    return JsonResponse({
        'disliked': True, 'default': default
    })
