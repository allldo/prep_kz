from itertools import chain

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product, Cart, ProductCartItem, Category, City, Address, Review
from .forms import  RegisterForm
from .service import log_in, get_customer, get_cart
from django.db.models import Q



def main_page(request: WSGIRequest) -> HttpResponse:
    """ Главная страница магазина """
    context = {'products': Product.objects.all()}
    return render(request, 'shop/main.html', context)


def product_detail(request: WSGIRequest, product_id: int, product_slug: str) -> HttpResponse:
    """ Страница отдельного товара """
    context = {'product': get_object_or_404(Product, id=product_id, slug=product_slug)}
    return render(request, 'shop/product_detail.html', context)


def category_detail(request, category_slug: str):
    """ Страница фильтра """
    category = get_object_or_404(Category, slug=category_slug)
    products_ordered_by_price = Product.objects.all().order_by('-price')
    highest_price = products_ordered_by_price.first()
    lowest_price = products_ordered_by_price.last()
    context = {'highest_price': highest_price, 'lowest_price': lowest_price, 'all_categories': Category.objects.all()}
    context['category']: category

    filtered = Category.objects.filter(slug=category_slug).first().product.all().order_by('-price')[:15]
    context = {'filtered': filtered}
    return render(request, 'shop/category_detail.html', context)


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


def log_out(request: WSGIRequest):
    """ Выход с аккаунта """
    logout(request)
    return HttpResponseRedirect(reverse('shop:main_page'))


def register(request: WSGIRequest):
    """ Регистрация """
    # if request.user.is_authenticated:
    #     return redirect('company:profile')
    context = {}
    if request.POST:
        user = User.objects.create(email=request.POST.get('email'),
                                   username=request.POST.get('username'), password=request.POST.get('password'))
        login(request, user)
        return HttpResponseRedirect(reverse('shop:lk'))

    form = RegisterForm()
    context['register_form'] = form
    return render(request, 'shop/register.html', context)


@require_POST
@login_required()
def add_to_cart(request: WSGIRequest) -> JsonResponse:
    """ Добавление товара в корзину """
    cart = get_object_or_404(Cart, cart_owner=get_customer(request))
    json_data = cart.add_product_to_cart(request.POST.get('product_id'), request.POST.get('quantity'))
    # product_item = ProductCartItem.objects.create(product=product, quantity=request.POST.get('quantity'))
    # cart.product_item.add(product_item.id)
    return JsonResponse({
        'added': True, 'product': {
            'name': json_data['name'],
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


def remove_from_cart(request: WSGIRequest) -> HttpResponse:
    """ Удаление товара из корзины """
    get_cart(request).delete_product_from_cart(request.POST.get('product_id'))
    return JsonResponse({
        'deleted': True
    })


def cart_detail(request: WSGIRequest) -> HttpResponse:
    """ Страница корзины """
    customer = get_customer(request)
    context = {
        'customer': customer,
        'cart': customer.get_cart()
    }
    return render(request, 'shop/cart_page.html', context)


@login_required()
def lk(request):
    context = {
        'sidebar_val': 1,
        'customer': get_customer(request)
    }
    return render(request, 'lk/lk.html', context)


# redirect_field_name='/login/'
@login_required()
def addresses(request: WSGIRequest) -> HttpResponse:
    customer = get_customer(request)
    if request.method == 'POST':
        city = request.POST.get('city')
        num_of_house = request.POST.get('number_of_house')
        floor = request.POST.get('floor')
        flat = request.POST.get('flat')
        Address.objects.create(customer=customer, city=City.objects.get(name=city), floor=floor, flat=flat,
                               house=num_of_house)
        return HttpResponseRedirect(reverse('shop:addresses'))
    context = {
        'sidebar_val': 2,
        'customer': get_customer(request),
        'cities': City.objects.all(),
        'addresses': Address.objects.filter(customer=customer)
    }
    return render(request, 'lk/lk_address.html', context)


@require_POST
def delete_address(request):
    address = request.POST.get('address_id')
    get_object_or_404(Address, id=address).delete()
    return JsonResponse({
        'deleted': True,
        'address_id': address
    })


# redirect_field_name='/login/'
@login_required()
def history(request: WSGIRequest) -> HttpResponse:
    context = {
        'sidebar_val': 3,
        'customer': get_customer(request)
    }
    return render(request, 'lk/lk_history.html', context)


# redirect_field_name='/login/'
@login_required()
def current_delivery(request: WSGIRequest) -> HttpResponse:
    context = {
        'sidebar_val': 4,
        'customer': get_customer(request)
    }
    return render(request, 'lk/lk_delivery.html', context)


# redirect_field_name='/login/'
@login_required()
def wishlist(request: WSGIRequest) -> HttpResponse:
    context = {
        'sidebar_val': 5,
        'customer': get_customer(request)
    }
    return render(request, 'lk/lk_wishlist.html', context)


# redirect_field_name='/login/'
@login_required()
def reviews(request: WSGIRequest) -> HttpResponse:
    customer_reviews = Review.objects.filter(user=get_customer(request))
    context = {
        'sidebar_val': 6,
        'customer': get_customer(request),
        'reviews': customer_reviews
    }
    return render(request, 'lk/lk_reviews.html', context)


@require_POST
def delete_review(request):
    review_id = request.POST.get('review_id')
    get_object_or_404(Review, id=review_id).delete()
    return JsonResponse({
        'deleted': True,
        'review_id': review_id
    })

