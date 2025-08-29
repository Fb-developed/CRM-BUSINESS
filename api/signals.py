from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Notification

@receiver(post_save, sender=Product)
def notify_product_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.shop.user,
            message=f"Маҳсулоти нав '{instance.name}' ба магазин '{instance.shop.name}' илова шуд."
        )
