"""Manage Admin interface for the e-commerce application."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin   
from django.utils.translation import gettext_lazy as _

from coreapp import models

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


    
class PropertyAdmin(admin.ModelAdmin):
    """Define the admin pages for properties."""
    list_display = ['name', 'price', 'owner', 'property_type', 'category']
    search_fields = ['name', 'owner__username']
    list_filter = ['property_type', 'category']
    ordering = ['-created_at']
    list_per_page = 20
    fieldsets = (
        (None, {'fields': ('name', 'description', 'price', 'owner', 'type', 'category')}),
        (_('Contact Info'), {'fields': ('contact_number', 'contact_email')}),
        (_('Property Details'), {'fields': ('bedrooms', 'bathrooms', 'parking_spaces')}),
    )

class MessageAdmin(admin.ModelAdmin):
    """Define the admin pages for messages."""
    list_display = ['rent', 'message', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['-created_at']
    list_per_page = 20
    fieldsets = (
        (None, {'fields': ('name', 'email', 'message')}),
        (_('Contact Info'), {'fields': ('phone_number',)}),
    )
    
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Rent, PropertyAdmin)
admin.site.register(models.Contact, MessageAdmin)
