from django.contrib import admin
from .models import Product, Category, Customer, Review, Cart, ProductCartItem, City, Address


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cart)
admin.site.register(ProductCartItem)
admin.site.register(City)
admin.site.register(Address)
