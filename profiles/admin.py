from django.contrib import admin
from .models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    list_filter = ['username', 'first_name', 'last_name', 'email', 'phone_number']
admin.site.register(UserProfile, UserProfileAdmin)






