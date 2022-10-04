from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product, Cart, ProductCartItem
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


def login_user(request):
    """ Функция для отработки логина в систему """
    if request.method == 'GET':
        return render(request, 'shop/login_page.html')
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
def add_to_cart(request: WSGIRequest) -> JsonResponse:
    """ Добавление товара в корзину """
    cart = get_object_or_404(Cart, cart_owner=get_customer(request))
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    product_item = ProductCartItem.objects.create(product=product, quantity=request.POST.get('quantity'))
    cart.product_item.add(product_item.id)
    print(cart.total_sum())
    return JsonResponse({
        'added': True, 'product': {
            'name': product.name,
            'quantity': request.POST.get('quantity')
        }

    })


@csrf_exempt
def add_to_wishlist(request: WSGIRequest):
    """ Добавить товар в список желаемого """
    customer = get_customer(request)
    if not customer:
        return JsonResponse({
            'redirect': True
        })
    product_id = request.POST.get('product_id')
    product_id = product_id[:-8]
    customer.wishlist.add(product_id)
    return JsonResponse({
        'added': True, 'product_id': product_id
    })


@csrf_exempt
def remove_from_wishlist(request: WSGIRequest):
    """ Добавить товар в список желаемого """
    customer = get_customer(request)
    if not customer:
        return JsonResponse({
            'redirect': True
        })
    product_id = request.POST.get('product_id')
    product_id = product_id[:-8]
    customer.wishlist.remove(product_id)
    return JsonResponse({
        'removed': True, 'product_id': product_id
    })


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
