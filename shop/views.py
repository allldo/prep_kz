from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product
from .cart import Cart
from .forms import CartAddProductForm, RegisterForm
from .service import log_in, get_customer


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
def login_user(request):
    """ Функция для отработки логина в систему """
    if log_in(request, request.POST.get('username'), request.POST.get('password')):
        return JsonResponse({
            'logged': True,
            'username': request.POST.get('username')
        })
    else:
        return JsonResponse({
            'logged': False, 'reason': 'Wrong credentials'
        })


def lk(request):
    return render(request, 'lk/lk.html')


def log_out(request: WSGIRequest):
    """ Выход с аккаунта """
    logout(request)


def register(request: WSGIRequest):
    """ Регистрация """
    # if request.user.is_authenticated:
    #     return redirect('company:profile')
    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        context['form_errors'] = form.errors
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:lk')

    form = RegisterForm()
    context['register_form'] = form
    return render(request, 'shop/register.html', context)


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


@csrf_exempt
@login_required
def add_to_wishlist(request: WSGIRequest):
    customer = get_customer(request)
    product_id = request.POST.get('product_id')
    # customer.wishlist


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
