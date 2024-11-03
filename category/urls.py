from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.categories_test, name='test'),  # Test view for categories
    path('register/', views.register_category, name='register_category'),  # View to register a new category
    path('search/', views.search_categories, name='search_categories'),  # View to search for categories
    path('manage/', views.manage_categories, name='manage_categories'),  # View to manage categories
    path('update/<int:category_id>/', views.update_category, name='update_category'),  # View to update a category
    path('delete/<int:category_id>/', views.delete_category, name='delete_category'),  # View to confirm deletion of a category
]
