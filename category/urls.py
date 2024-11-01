from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.categories_test, name='test'),  # Test view for categories
    path('register/', views.register_category, name='register_category'),  # View to register a new category
    path('search/', views.search_categories, name='search_category'),  # View to search for categories
    path('manage/', views.manage_categories, name='manage_categories'),  # View to manage categories
]
