from django.contrib import admin
from .models import Post
from .models import Home



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} 


admin.site.register(Post, PostAdmin)


class HomeAdmin(admin.ModelAdmin):
    list_display = ('total_rewards', 'total_investor', 'total_withdraw', 'total_transaction')
    list_filter = ('total_rewards', )
    search_fields = ('total_rewards', 'total_investor', 'total_withdraw', 'total_transaction')
    ordering = ('total_rewards',)
admin.site.register(Home, HomeAdmin)

