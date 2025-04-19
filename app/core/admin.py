"""Manage Admin interface for the e-commerce application."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin   
from django.utils.translation import gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []
    list_per_page = 20
    def get_queryset(self, request):
        """Override the queryset to include all users."""
        return super().get_queryset(request).select_related('user_permissions')
    
admin.site.register(models.User, UserAdmin)