from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.items_test, name='test'),
    path('register_item/', views.register_item, name='register_item'),
    path('search_items/', views.search_items, name='search_items'),
    path('manage_inventory/', views.manage_inventory, name='manage_inventory'),
]
