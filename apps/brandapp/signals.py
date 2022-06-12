from datetime import datetime
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from brandapp.models import  BrandPromotion


@receiver(pre_save, sender=BrandPromotion)
def pre_save(sender, instance, **kwargs):
    '''
    This function is called before the save() method of the model.
    it will check if the promotion is active or not.

    '''
    if instance.is_active:
        if instance.promotion_type == 1:
            if instance.number_of_users <= instance.reach_counts:
                instance.is_active = False
            elif instance.promotion_type == 2:
                if instance.valid_to < datetime.now():
                    instance.is_active = False
            instance.save()
    