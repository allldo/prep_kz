from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import get_object_or_404
from typing import Union

from .models import Customer


def log_in(request: WSGIRequest, username: str, password: str) -> bool:
    """ Функция входа """
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False


def get_customer(request: WSGIRequest) -> Union[Customer, bool]:
    """ Получение юзера (залогиненного) """
    if isinstance(request.user, AnonymousUser):
        return False
    customer = get_object_or_404(Customer, user=request.user)
    return customer


def get_cart(request: WSGIRequest):
    """ Получение корзины """
    return get_customer(request).get_cart()
