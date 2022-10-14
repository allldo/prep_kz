from django.contrib import admin
from django.urls import path
from .views import add_to_cart, remove_from_cart, cart_detail, main_page, category_detail, product_detail, login_user,\
    register, log_out, lk, add_to_wishlist, remove_from_wishlist, addresses, history, current_delivery, wishlist,\
    reviews, delete_address, delete_review
app_name = 'shop'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', login_user, name='login'),
    path('lk/', lk, name='lk'),
    path('register/', register, name='register'),
    path('logout/', log_out, name='logout'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/', remove_from_wishlist, name='remove_from_wishlist'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('category/<slug:category_slug>', category_detail, name='product_list_by_category'),
    path('shop/<int:product_id>/<slug:product_slug>', product_detail, name='product_detail'),

    # Личный кабинет
    path('shop/lk/addresses/', addresses, name='addresses'),
    path('shop/lk/addresses/delete_address', delete_address, name='delete_address'),
    path('shop/lk/history/', history, name='history'),
    path('shop/lk/current_delivery', current_delivery, name='current_delivery'),
    path('shop/lk/wishlist', wishlist, name='wishlist'),
    path('shop/lk/reviews', reviews, name='reviews'),
    path('shop/lk/reviews/delete_review', delete_review, name='delete_review'),
]
