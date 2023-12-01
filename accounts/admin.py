from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import User
from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined',)
    fieldsets = (
        ('Основная информация',
         {'fields': ('username', 'email', 'name', 'password',)}),
        ('Права', {'fields': ('is_staff', 'is_active', 'is_superuser',)}),
    )
    add_fieldsets = (
        ('Основная информация',
         {'fields': ('username', 'email', 'name', ('password1', 'password2',),)}),
        ('Права', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    search_fields = ('username', 'email', 'name', 'date_joined',)
    ordering = ('username', 'email', 'name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')


admin.site.register(User, CustomUserAdmin)
