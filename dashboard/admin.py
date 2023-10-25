from django.contrib import admin
from .models import Account, DepositHistory, WithdrawalHistory

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'ultimate_balance', 'selected_plan_name', 'total_payout', 'total_deposit', 'pending_amount', 'interest_earn', 'total_earning', 'referral_earnings', 'lifetime_bonus']
    search_fields = ['user_profile__user__username',]
    list_filter = ['user_profile',]
    
    def selected_plan_name(self, obj):
        return obj.get_selected_plan_display()
    
    selected_plan_name.short_description = 'Selected Plan'
admin.site.register(Account, AccountAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('get_transaction_id', 'get_user_username', 'selected_plan', 'deposit_amount', 'transaction_date', 'status')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'user_profile__user__username', 'selected_plan', 'status')

    def get_transaction_id(self, obj):
        # Extract only the numeric part of the transaction ID without "TRANS"
        return obj.transaction_id[5:]

    get_transaction_id.short_description = 'Transaction ID' # Set column header name in the admin panel

    def get_user_username(self, obj):
        return obj.user_profile.user.username

    get_user_username.short_description = 'User' # Set column header name in the admin panel

admin.site.register(DepositHistory, TransactionAdmin)

class WithdrawalHistoryAdmin(admin.ModelAdmin):
    list_display = ['get_transaction_id', 'user_profile', 'withdraw_amount', 'withdrawal_date', 'status']
    search_fields = ['user_profile__user__username', 'transaction_id']
    list_filter = ['status']

    def get_transaction_id(self, obj):
        # Extract only the numeric part of the transaction ID without "TRANS"
        return obj.transaction_id[5:]

    get_transaction_id.short_description = 'Transaction ID' # Set column header name in the admin panel

admin.site.register(WithdrawalHistory, WithdrawalHistoryAdmin)


