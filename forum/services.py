from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404

from forum.models import Comment
from shop.service import get_customer


def plural_time(number: int, type_time: str):
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


def like_or_dislike(request: WSGIRequest, comment_pk: int, like: bool):
    """ """
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
