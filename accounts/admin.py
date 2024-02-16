from django.contrib import admin

from accounts.models import Account, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ["user", "balance", "created_date"]

class TransactionAdmin(admin.ModelAdmin):
    list_display = ["account", "amount", "transaction_type", "created_date"]

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)