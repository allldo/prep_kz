from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer, Cart, Review


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)
        Cart.objects.create(cart_owner=customer)


@receiver(post_save, sender=Review)
def create_review(sender, instance, created, **kwargs):
    if created:
        instance.product.set_score()

