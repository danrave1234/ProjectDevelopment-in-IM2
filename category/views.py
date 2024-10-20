from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def category_test(request):
    return HttpResponse("<h1>Hello, this is the views for category</h1>")