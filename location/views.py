from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def location_test(request):
    return HttpResponse("<h1>Hello, this is the views for location</h1>")