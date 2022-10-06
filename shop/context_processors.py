from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404

from .models import Cart
from .service import get_customer


def cart(request):
    cart_owner = get_customer(request)
    if cart_owner:
        cart_q = get_object_or_404(Cart, cart_owner=cart_owner)
        return {
            'cart': cart_q
        }
    return request
