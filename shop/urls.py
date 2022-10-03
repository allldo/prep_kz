from django.contrib import admin
from django.urls import path
from .views import add_to_cart, remove_from_cart, cart_detail, main_page, category_detail, product_detail, login_user, register
app_name = 'shop'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('category/<slug:category_slug>', category_detail, name='product_list_by_category'),
    path('shop/<int:product_id>/<slug:product_slug>', product_detail, name='product_detail')
]
