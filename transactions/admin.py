from django.contrib import admin

from .models import Transaction

# Transaction admin
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'account', 
        'amount', 
        'transaction_type', 
        'created_date'
    ]


admin.site.register(Transaction, TransactionAdmin)
