from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.service import get_customer
from .serializers import ProductSerializer
from shop.models import Product, ProductCartItem


@api_view(['GET'])
def get_product_info(request: WSGIRequest):
    product_pk = request.GET.get('product_pk')
    product = get_object_or_404(Product, pk=product_pk)
    customer = get_customer(request)
    serialized_product = ProductSerializer(product).data
    wishlisted = True if product in customer.wishlist.all() else False
    in_cart = True if ProductCartItem.objects.filter(customer=customer, product_id=product_pk).exists() else False
    return Response({
        'product': serialized_product, 'wishlisted': wishlisted, 'in_cart': in_cart
    })


@api_view(['POST'])
def clear_cart(request: WSGIRequest) -> HttpResponse:
    customer = get_customer(request)
    customer.get_cart().clear_cart()
    return Response({
        'deleted': True
    })


@api_view(['POST'])
def lk_change_info(request: WSGIRequest) -> HttpResponse:
    customer = get_customer(request)
    username, name, surname, phone_number = request.POST.get('username'), request.POST.get('name'), \
                                            request.POST.get('surname'), request.POST.get('phone_number')
    customer.set_params(username=username, name=name, surname=surname, phone_number=phone_number)
    return Response({
        'changed': True
    })
