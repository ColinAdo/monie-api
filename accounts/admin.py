from django.contrib import admin

from accounts.models import Account

# Account admin
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'name', 
        'description', 
        'balance', 
        'created_date'
    ]

admin.site.register(Account, AccountAdmin)

