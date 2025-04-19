"""
URL mapping for the user API.
"""
from typing import List
from django.urls import path, URLPattern
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

app_name = 'user'

urlpatterns: List[URLPattern] = [
    # The above code defines the URL patterns for the user-related API endpoints in a Django application.
    # Does not authenticate the user.
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    # The login URL is used to authenticate users and obtain a token for accessing protected resources.
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('list/', views.UserListView.as_view(), name='user_list'),
]