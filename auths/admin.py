from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auths.models import CustomUser

# Custom user admin 
class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "is_active",
        "is_superuser",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
