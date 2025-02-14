from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
         if not hasattr(instance, 'customer'):  # Only create the customer when the user is first created
            Customer.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email
            )

@receiver(post_save, sender=User)
def update_customer(sender, instance, **kwargs):
    try:
        customer = instance.customer
        customer.first_name = instance.first_name
        customer.last_name = instance.last_name
        customer.email = instance.email
        customer.save()
    except Customer.DoesNotExist:
        pass
