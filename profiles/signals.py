import random
import string
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile
from dashboard.models import Account

def generate_referral_code():
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(8))


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        referral_code = generate_referral_code()
        UserProfile.objects.create(user=instance, username=instance.username, email=instance.email, referral_code=referral_code)


@receiver(post_delete, sender=UserProfile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


