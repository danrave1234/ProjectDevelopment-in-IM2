from django.shortcuts import render
from django.http import HttpResponse

def user_test(request):
    return HttpResponse("<h1>Hello, this is the views for user</h1>")

