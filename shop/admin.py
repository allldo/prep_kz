from django.contrib import admin
from .models import Product, Category, Customer, Review, Cart, ProductCartItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(ProductCartItem)