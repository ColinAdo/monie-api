from django.contrib import admin

from .models import Transaction, Chat

# Transaction admin
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'account', 
        'amount', 
        'transaction_type', 
        'description',
        'created_date'
    ]

class ChatAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'prompt',
        'response', 
    ]


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Chat, ChatAdmin)
