from django.urls import path

from location.views import location_test

urlpatterns = [
    path('test/', location_test, name='location'),
]