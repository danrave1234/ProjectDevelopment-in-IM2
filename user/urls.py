from django.urls import path

from .views import user_test

urlpatterns = [
    path('test/', user_test, name='user'),
]