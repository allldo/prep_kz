from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models.query import QuerySet
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField('shop.Product', null=True, blank=True)
    name = models.CharField(max_length=125, null=True, blank=True)
    surname = models.CharField(max_length=125, null=True, blank=True)
    phone_number = models.CharField(max_length=125, null=True, blank=True)

    def __str__(self):
        """ Имя пользователя """
        return self.user.username

    def get_cart(self):
        """ Получение корзины """
        return get_object_or_404(Cart, cart_owner=self)

    def is_authenticated(self):
        """ Для шаблона """
        return True

    def is_empty_wishlist(self):
        """ Проверка есть ли желаемые продукты """
        return True if self.wishlist.all().count() == 0 else False

    def does_have_address(self):
        """ Проверка есть ли адреса у кастомера """
        return True if Address.objects.filter(customer=self).exists() else False

    def set_params(self, **kwargs):
        self.user.username = kwargs['username']
        self.name = kwargs['name']
        self.surname = kwargs['surname']
        self.phone_number = kwargs['phone_number']
        self.save()


class Address(models.Model):
    customer = models.ForeignKey('shop.Customer', on_delete=models.CASCADE, related_name='customer')
    city = models.ForeignKey('shop.City', on_delete=models.CASCADE, related_name='city')
    house = models.CharField(max_length=100)
    floor = models.IntegerField()
    flat = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.customer, self.city


class City(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class Category(models.Model):
    product = models.ManyToManyField('Product',
                                     related_name='products', null=True, blank=True)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """ Получение названия категории """
        return self.name

    def get_absolute_url(self):
        """ Уникальная ссылка для категории """
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):

    name = models.CharField(max_length=150, db_index=True)
    slug = models.CharField(max_length=150, db_index=True, unique=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    image_on_hover = models.ImageField(upload_to='product/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)
    rating = models.FloatField(null=True, blank=True)

    # Тут пипл вотед для формулы после которой показывать рейтинг
    people_voted = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'), )

    def __str__(self) -> str:
        """ Получение названия товара """
        return self.name

    def get_product_categories(self) -> QuerySet:
        """ Позволяет получить все категории товара """
        categories = Category.objects.filter(product=self)
        return categories if categories.count() > 0 else None

    def get_absolute_url(self):
        """ Уникальная ссылка для товара """
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_score(self):
        """ Получение рейтинга продукта """
        rt = self.rating
        return str(rt)

    def set_score(self):
        """ Подсчет рейтинга продукта """
        reviews_related = Review.objects.filter(product=self)
        if reviews_related.exists():
            reviews_total = reviews_related.count()
            self.rating = reviews_related.aggregate(Sum('rating'))['rating__sum'] / reviews_total

    def get_reviews_number(self):
        """ Количество отзывов """
        return Review.objects.filter(product=self).count()

    def get_reviews(self):
        """ Получение отзывов """
        return Review.objects.filter(product=self)


class Review(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    email = models.EmailField(max_length=120, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        """ String representation of review """
        return self.user.user.username

    def get_rating(self):
        """ Получение рейтинга в формате приемлимом для js либы """
        return str(self.rating).replace(',', '.')


class Cart(models.Model):
    cart_owner = models.ForeignKey('shop.Customer', on_delete=models.CASCADE)
    # products = models.ManyToManyField('shop.Product', null=True, blank=True)
    product_item = models.ManyToManyField('shop.ProductCartItem', null=True, blank=True)

    def __str__(self):
        return 'Корзина ' + self.cart_owner.user.username

# TODO потенциально в селери таск

    def total_sum(self):
        """ Стоимость всех товаров в корзине """
        total = 0
        for product_item in self.product_item.all():
            total += product_item.get_total_by_product()
        return total

    def get_all_products_in_cart(self):
        """ Получение всех продуктов в корзине """
        return self.product_item.select_related('product')

    def total_products_in_cart(self):
        """ Общее количество продуктов в корзине """
        return self.product_item.all().count()

    def delete_product_from_cart(self, product_id):
        """ Удаление товара из корзины """
        ProductCartItem.objects.get(product_id=product_id, cart=self, customer=self.cart_owner).delete()

    def add_product_to_cart(self, product_id, quantity):
        """ Добавление в корзину """
        product = get_object_or_404(Product, id=product_id)
        try:
            item = ProductCartItem.objects.get(product=product, customer=self.cart_owner)
            item.quantity += int(quantity)
            item.save()
        except:
            new_product = ProductCartItem.objects.create(product=product, customer=self.cart_owner, quantity=quantity)
            self.product_item.add(new_product)
        json_return = {'name': product.name}
        return json_return

    def clear_cart(self):
        """ Полная очистка корзины """
        ProductCartItem.objects.filter(cart=self, customer=self.cart_owner).delete()
# class ProductOptions(models.Model):
#     SIZES_CHOICES = (
#
#     )
#     COLOR_CHOICES = (
#
#     )
#     brand =
#     weight =
#     size =
#     color =


class ProductCartItem(models.Model):
    customer = models.ForeignKey('shop.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        """ Название единицы товара """
        return self.product.name + ' в количестве '+str(self.quantity)

    def get_total_by_product(self):
        """ Подсчет суммы по этой единицы """
        return self.quantity*self.product.price
