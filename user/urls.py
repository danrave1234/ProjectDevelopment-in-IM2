from django.urls import path
from . import views

urlpatterns = [
    # Authentication paths
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('welcome/', views.welcome_view, name='welcome'),

    # User profile path
    path('profile/', views.profile_view, name='profile'),

    # Admin-only user management paths
    path('admin/users/', views.list_users, name='list_users'),
    path('admin/users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/users/manage/', views.manage_users, name='manage_users'),
]
