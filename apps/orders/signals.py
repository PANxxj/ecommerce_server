from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.helper import functions
from . import models as order_models
from datetime import timedelta
import uuid
from django.utils import timezone

@receiver(post_save, sender=order_models.OrderData)
def create_ref_id(sender, instance, created, **kwargs):
    if created: 
        order_count = order_models.OrderData.objects.filter(customer = instance.customer).count()
        ref_id = f"ORD{order_count + 1:04d}"  # eg. ODG00001, ODG00002, ...
        instance.order_id = ref_id
        instance.dod =(timezone.now() + timedelta(days=7)).date()
        instance.tracking_number = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        instance.save() 
        
        steps = functions.return_steps()
        for step in steps:
            order_models.OrderStep.objects.create(
                odering = step['id'],
                order = instance,
                status = step['status'],
                description = step['description']
            )
        
        
        