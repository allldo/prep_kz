from django.shortcuts import get_object_or_404

from .models import Cart
from .service import get_customer


def cart(request):
    cart_q = get_object_or_404(Cart, cart_owner=get_customer(request))
    return cart_q


