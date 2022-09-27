from django.contrib import admin
from django.urls import path
from .views import add_to_cart, remove_from_cart, cart_detail, main_page
app_name = 'shop'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_detail, name='cart_detail'),

]
