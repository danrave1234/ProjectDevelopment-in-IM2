from django.urls import path
from . import views

urlpatterns = [
    path('register_item/', views.register_item, name='register_item'),
    path('search_items/', views.search_items, name='search_items'),
    path('manage_inventory/', views.inventory_management, name='manage_inventory'),
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Add this line

]
