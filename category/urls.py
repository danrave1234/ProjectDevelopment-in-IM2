
from django.urls import path

from category.views import category_test

urlpatterns = [
    path('test/', category_test, name='category'),
]