from django.db import models
from profiles.models import UserProfile 

# Create your models here.
class Account(models.Model):
    PLAN_CHOICES = (
        ('Basic','Basic Plan'),
        ('Standard','Standard Plan'),
        ('Silver','Silver Plan'),
        ('Premium','Premium Plan'),
        ('Gold','Gold Plan'),
        ('Diamond','Diamond Plan'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    selected_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='Basic')
    ultimate_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_earn = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referral_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lifetime_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=False)
    


    def credit_referral_earnings(self, referral_earnings):
        self.referral_earnings += referral_earnings
        self.save()

    def save(self, *args, **kwargs):
        if self.is_active:
            self.ultimate_balance = (
                self.interest_earn + self.total_earning + self.referral_earnings + self.lifetime_bonus
            )
        super(Account, self).save(*args, **kwargs)

class DepositHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    selected_plan = models.CharField(max_length=20, choices=Account.PLAN_CHOICES)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Account.STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.transaction_id} - {self.user_profile.user.username}"

class WithdrawalHistory(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    )
    transaction_id = models.CharField(max_length=20, unique=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    withdraw_amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawal_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.transaction_id[5:]
    
class Withdrawal(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    withdrawal_history = models.ForeignKey(WithdrawalHistory, on_delete=models.CASCADE)
    withdrawal_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


