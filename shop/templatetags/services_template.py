from django.shortcuts import get_object_or_404

from ..models import Product
from ..service import get_customer
from django import template
register = template.Library()


@register.simple_tag
def is_product_in_wishlist(request, product_pk) -> bool:
    """ Есть ли продукт в вишлисте юзера """
    customer = get_customer(request)
    if not customer:
        return False
    product = get_object_or_404(Product, pk=product_pk)
    if product in customer.wishlist.all():
        return True
    return False
