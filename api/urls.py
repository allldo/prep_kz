from django.urls import path

from api.views import get_product_info, clear_cart, lk_change_info

app_name = 'api'
urlpatterns = [
        path('get_product_info/', get_product_info, name='get_product_info'),
        path('clear_cart/', clear_cart, name='clear_cart'),
        path('lk_change_info/', lk_change_info, name='lk_change_info'),
]
