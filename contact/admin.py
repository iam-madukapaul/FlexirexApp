from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['name', 'email']
    fields = ['name', 'email', 'message'] 

admin.site.register(Contact, ContactAdmin)




