from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from shop.models import Product


@api_view(['GET'])
def get_product_info(request: WSGIRequest):
    product_pk = request.GET.get('product_pk')
    serialized_product = ProductSerializer(get_object_or_404(Product, pk=product_pk)).data
    return Response({
        'product': serialized_product
    })
