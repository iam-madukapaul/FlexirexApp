from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    email_verified = models.BooleanField(default=False) 
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    usdt_wallet = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='img', default='default.jpg')
    username = models.CharField(max_length=200)
    email = models.EmailField()
    referral_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
 
    def __str__(self):
        return self.username
    

    

