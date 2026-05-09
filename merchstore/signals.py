from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction

@receiver(post_save, sender=Transaction)
def update_stock_on_transaction(sender, instance, created, **kwargs):
    if created:
        product = instance.Product_Bought
        if product.stock > 0:
            product.stock -= instance.Amount
            product.save()