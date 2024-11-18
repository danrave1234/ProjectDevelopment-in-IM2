from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('signup/', views.signup_view, name='signup'),
    path('homepage/', views.homepage_view, name='homepage'),
    path('admin-login/', views.admin_login_view, name='admin-login'),

    # Admin-only user management paths
    path('users/', views.list_users, name='list_users'),  # Lists all users
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),  # Updates a specific user
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # Deletes a specific user
    
    # Manage users path
    path('manage_users/', views.manage_users, name='manage_users'),
]