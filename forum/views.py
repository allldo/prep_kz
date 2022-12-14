from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from shop.service import get_customer
from .decorators import requires_admin
from .models import Post, Comment, Topic, Ip, Report, Notification
from shop.models import Customer

from .services import like_or_dislike, get_client_ip, split_id, get_username_or_none

from .forms import TinyForm, TinyCommentForm

from django.core.paginator import Paginator


def main_forum(request: WSGIRequest) -> HttpResponse:
    """ Main forum page """
    context = {'latest_comment': Comment.objects.all().order_by('-date')[:3],
               'total_posts': Post.objects.all().count(),
               'total_comments': Comment.objects.all().count(),
               'total_users': Customer.objects.all().count(),
               'topics': Topic.objects.all(),
               'customer': get_customer(request)}
    # total users добавить флаг у кастомера на активность на форуме
    return render(request, 'forum/forum_main.html', context)


def topic(request: WSGIRequest, topic_id: int) -> HttpResponse:
    """ Topic page """
    top_ic = get_object_or_404(Topic, pk=topic_id)
    posts = top_ic.get_posts()
    paginator = Paginator(posts, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'topic': top_ic,
        'page_obj': page_obj
    }
    return render(request, 'forum/topic_page.html', context)


def create_post(request: WSGIRequest, topic_name: str) -> HttpResponse:
    """ Creating post view """
    form = TinyForm()
    top_ic = get_object_or_404(Topic, title=topic_name)
    context = {
        'form': form,
        'topic': top_ic,
    }
    return render(request, 'forum/create_post.html', context)


@require_POST
def new_post(request: WSGIRequest, topic_name: str) -> HttpResponse:
    """ Creating post then redirecting to it """
    top_ic = get_object_or_404(Topic, title=topic_name)
    post = Post.objects.create(topic=top_ic, author=get_customer(request),
                               name=request.POST.get('post_name'),
                               content=request.POST.get('content'))
    return HttpResponseRedirect(reverse('forum:post_detail', kwargs={
        'post_id': post.pk
    }))


@require_POST
def new_comment(request:WSGIRequest, post_name: str) -> HttpResponse:
    """ creating comment then refreshing page (?) """
    content = request.POST.get('content')

    post = get_object_or_404(Post, name=post_name)
    comment = Comment.objects.create(post=post, author=get_customer(request),
                                     content=content)
    Notification.create_notification(
        get_username_or_none(content),
        comment
    )
    return HttpResponseRedirect(reverse('forum:post_detail', kwargs={
        'post_id': post.pk
    }))


def post_detail(request: WSGIRequest, post_id: int) -> HttpResponse:
    """ Post detail page with pagination """
    post = get_object_or_404(Post, id=post_id)
    ip = get_client_ip(request)

    if Ip.objects.filter(ip=ip).exists():
        post.views.add(Ip.objects.get(ip=ip))
    else:
        ip = Ip.objects.create(ip=ip)
        post.views.add(ip)

    form = TinyCommentForm()
    paginator = Paginator(post.get_comments(), 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post': post,
        'topic': post.topic,
        'page_obj': page_obj,
        'form': form,
        'customer': get_customer(request)
    }
    return render(request, 'forum/post_detail.html', context)


@require_POST
def like(request: WSGIRequest, post_id: int) -> JsonResponse:
    """ Like view w/o refreshing the page """
    comment, default = like_or_dislike(request, request.POST.get('comment_pk'), True)
    return JsonResponse({
        'liked': True, 'default': default, 'comment_pk': comment.pk
    })


@require_POST
def dislike(request: WSGIRequest, post_id: int) -> JsonResponse:
    """ Dislike view w/o refreshing the page """
    comment, default = like_or_dislike(request, request.POST.get('comment_pk'), False)
    return JsonResponse({
        'disliked': True, 'default': default, 'comment_pk': comment.pk
    })


@require_POST
def submit_report(request: WSGIRequest, post_id: int) -> JsonResponse:
    """ Report submitting view """
    item_id, item_type = split_id(request.POST.get('report'))
    report_body = request.POST.get('body')
    customer = get_customer(request)
    if item_type == 'comment':
        Report.objects.create(report_body=report_body, from_user=customer, comment=get_object_or_404(Comment, id=item_id))
    else:
        Report.objects.create(report_body=report_body, from_user=customer,
                              post=get_object_or_404(Post, id=item_id))
    return JsonResponse({
        'submitted': True
    })


@require_POST
def delete_content(request: WSGIRequest, post_id: int) -> Union[JsonResponse, HttpResponse]:
    """ Delete post or comment """
    item_id, item_type = split_id(request.POST.get('delete_message'))
    if item_type == 'comment-delete':
        get_object_or_404(Comment, id=item_id).delete()
        return JsonResponse({
            "item_id": item_id, "item_type": item_type
        })
    else:
        post = get_object_or_404(Post, id=item_id)
        topic_to_redirect = post.topic
        post.delete()
        return JsonResponse({
            'redirect': True, 'topic_id': topic_to_redirect.pk
        })

# @require_POST
# @requires_admin
# def ban_user(request):
