from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventory, Order

# Signal for low-stock alert
@receiver(post_save, sender=Inventory)
def check_low_stock(sender, instance, **kwargs):
    if instance.stock_level <= instance.reorder_threshold:
        print(f"Low Stock Alert: {instance.product.name} stock level is {instance.stock_level}.")

# Signal for new-order notification
@receiver(post_save, sender=Order)
def new_order_notification(sender, instance, created, **kwargs):
    if created:
        print(f"New Order Created: {instance.product.name}, Quantity: {instance.quantity}")
