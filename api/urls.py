from django.urls import path

from api.views import get_product_info

app_name = 'api'
urlpatterns = [
        path('get_product_info/', get_product_info, name='get_product_info'),
]
