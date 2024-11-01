from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.locations_test, name='test'),
    path('register/', views.register_location, name='register_location'),
    path('search/', views.search_locations, name='search_locations'),
    path('manage/', views.manage_locations, name='manage_locations'),
    path('update/<int:location_id>/', views.update_location, name='update_location'),
    path('delete/<int:location_id>/', views.delete_location, name='delete_location'),
]
