from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from shop.models import Product, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class ProductSerializer(ModelSerializer):
    get_reviews_number = serializers.ReadOnlyField(allow_null=True)
    get_product_categories = serializers.ReadOnlyField()

    class Meta:
        fields = '__all__'
        model = Product
