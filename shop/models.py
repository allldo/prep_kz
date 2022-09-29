from django.db import models
from django.urls import reverse
from django.db.models.query import QuerySet
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ForeignKey('shop.Product', on_delete=models.CASCADE, null=True, blank=True)


class Category(models.Model):
    product = models.ForeignKey('Product',
                                related_name='products',
                                on_delete=models.SET_NULL, null=True, blank=True)
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
        return Category.objects.filter(product=self)

    def get_absolute_url(self):
        """ Уникальная ссылка для товара """
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_score(self):
        """ Подсчет рейтинга продукта """
        return


class Review(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        """ String representation of review """
        return self.user, self.date if self.user else self.name, self.date
