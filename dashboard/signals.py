from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account

@receiver(post_save, sender=Account)
def update_ultimate_balance(sender, instance, **kwargs):
    if instance.is_active:
        instance.ultimate_balance = (
            instance.interest_earn + instance.total_earning + instance.referral_earnings + instance.lifetime_bonus
        )
        instance.save()