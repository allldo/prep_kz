from functools import wraps

from django.core.exceptions import PermissionDenied

from shop.service import get_customer


def requires_admin(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        customer = get_customer(request)
        if customer.is_admin:
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return decorated
