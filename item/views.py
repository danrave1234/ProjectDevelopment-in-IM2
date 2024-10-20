from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def items_test(request):
    return HttpResponse("<h1>Hello, this is the views for Items</h1>")
