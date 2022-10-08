from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction, Product

#! We are doing database related operations here, so we can return the warning message from serializers.

@receiver(pre_save, sender=Transaction)
def calculate_total_price(sender, instance, **kwargs):
    if not instance.price_total:
        instance.price_total = instance.quantity * instance.price

@receiver(post_save, sender=Transaction)
def update_stock(sender, instance, **kwargs):
    product = Product.objects.get(id=instance.product_id)
    if instance.transaction == 1:
        if not product.stock:
            #! first came as null so we did it like this 👆
            product.stock = instance.quantity
        else:
           product.stock += instance.quantity
    else:
        product.stock -= instance.quantity

    product.save()
