from django.contrib.auth import authenticate, login
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404

from .models import Customer


def log_in(request: WSGIRequest, username: str, password: str) -> bool:
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False


def get_customer(request: WSGIRequest) -> Customer:
    customer = get_object_or_404(Customer, user=request.user)
    return customer
