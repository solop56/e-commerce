"""
URL config for the admin
"""
from typing import List
from django.urls import path, URLPattern
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from property_admin import views

app_name = 'property_admin'

urlpatterns: List[URLPattern] = [
    path('register/', views.CreateAdminUserView.as_view(), name='admin_register'),
    path('login/', views.UserAdminLoginView.as_view(), name='admin_login'),
    path('logout/', views.UserAdminLogoutView.as_view(), name='admin_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='admin_token_refresh'),
    path('stats/', views.AdminListView.as_view(), name='list_of_users'),
    path('user/', views.AdminListView.as_view(), name='admin_user_detail'),
    path('stats/', views.AdminListView.as_view(), name='list_of_users'),
    path('user/', views.AdminListView.as_view(), name='admin_user_detail'),
    path('users/<str:pk>/', views.BanUserView.as_view(), name='ban_user'),
    ]