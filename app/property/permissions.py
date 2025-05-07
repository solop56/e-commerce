"""
Permissions for the property app.
"""

from rest_framework.permissions import BasePermission

class PropertyOwnerPermission(BasePermission):
    """
    Custom permission to only allow admin edit it.
    """

    def has_permission(self, request, view):
        """
        Check if the user is an admin.
        """
        return bool(request.user and request.user.is_admin_user and  getattr(request.user, 'is_admin_user', False)) 