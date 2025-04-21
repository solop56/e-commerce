"""
URL for property API.
"""
from typing import List

from django.urls import path, URLPattern

from property import views

app_name = 'property'



urlpatterns: List[URLPattern] = [
    # Property URLs
    path('create/', views.PropertyViewSet.as_view({'post': 'create'}), name='property_create'),
    path('update/<int:pk>/', views.PropertyViewSet.as_view({'put': 'update'}), name='property_update'),
    path('delete/<int:pk>/', views.PropertyViewSet.as_view({'delete': 'destroy'}), name='property_delete'),
    path('list/', views.PropertyListViewSet.as_view({'get': 'list'}), name='property_list'),
    path('search/', views.PropertyListViewSet.as_view({'get': 'search'}), name='property_search'),

    # Wishlist URLs
    path('saved/', views.WishlistViewSet.as_view({'get': 'list', 'post': 'create'}), name='wishlist'),
    path('wishlist/<int:pk>/', views.WishlistViewSet.as_view({'delete': 'destroy'}), name='wishlist_delete'),
    #path('wishlist/<int:pk>/update/', views.WishlistViewSet.as_view({'put': 'update'}), name='wishlist_update'),
    path('wishlist/<int:pk>/detail/', views.WishlistViewSet.as_view({'get': 'retrieve'}), name='wishlist_detail'),

]