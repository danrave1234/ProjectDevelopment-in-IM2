from item.views import items_test
from django.urls import path

urlpatterns = [
    path('test/', items_test, name='test')
]