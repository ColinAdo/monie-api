from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auths.forms import CustomUserCreationForm, CustomUserChangeForm
from auths.models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = [
        "username",
        "email",
        "phone_number",
        "is_active",
        "is_superuser",
    ]

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + \
        ((None, {"fields": ("phone_number",)}),)

admin.site.register(CustomUser, CustomUserAdmin)
