from typing import Tuple

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404

from forum.models import Comment
from shop.service import get_customer


def plural_time(number: int, type_time: str) -> str:
    """ Time in plural """
    if type_time == 'час':
        if number == 1:
            return '1 час назад'
        elif 1 < number < 5:
            return f'{number} часа назад'
        else:
            return f'{number} часов назад'
    elif type_time == 'минута':
        if number == 1:
            return '1 минуту назад'
        elif 1 < number < 5:
            return f'{number} минуты назад'
        else:
            return f'{number} минут назад'


def like_or_dislike(request: WSGIRequest, comment_pk: int, like: bool) -> Tuple[Comment, str]:
    """ Determining like or dislike """
    customer = get_customer(request)
    default = ''
    comment = get_object_or_404(Comment, id=comment_pk)
    if like:
        if customer in comment.dislikes.all():
            comment.dislikes.remove(customer)
            default = 'from dislike'
        if customer in comment.likes.all():
            default = 'already'
        comment.likes.add(customer)
        comment.save()
        return comment, default
    else:
        if customer in comment.likes.all():
            comment.likes.remove(customer)
            default = 'from like'
        if customer in comment.dislikes.all():
            default = 'already'
        comment.dislikes.add(customer)
        comment.save()
        return comment, default


def get_client_ip(request: WSGIRequest) -> str:
    """ Getting client ip for view counting """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
