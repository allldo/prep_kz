from django.db import models
from django.urls import reverse
from django.db.models.query import QuerySet


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
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)

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
