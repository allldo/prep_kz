from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product
from .cart import Cart
from .forms import CartAddProductForm


def main_page(request: WSGIRequest) -> HttpResponse:
    """ Главная страница магазина """
    context = {'products': Product.objects.all()}
    return render(request, 'shop/main.html', context)


def product_detail(request: WSGIRequest, product_id: int, product_slug: str) -> HttpResponse:
    """ Страница отдельного товара """
    context = {'product': get_object_or_404(Product, id=product_id, slug=product_slug)}
    return render(request, 'shop/product_detail.html', context)


def category_detail(request, category_slug: str):
    return render(request, 'shop/main.html')


@require_POST
def add_to_cart(request: WSGIRequest, product_id: int) -> HttpResponse:
    """ Добавление товара в корзину """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def remove_from_cart(request: WSGIRequest, product_id: int) -> HttpResponse:
    """ Удаление товара из корзины """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request: WSGIRequest) -> HttpResponse:
    """ Страница корзины """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'shop/card_detail.html', {'cart': cart})
