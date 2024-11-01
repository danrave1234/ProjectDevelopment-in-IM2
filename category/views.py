from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Category

# Test view
def categories_test(request):
    return HttpResponse("<h1>Hello, this is the views for Categories</h1>")

# Register a new category
def register_category(request):
    if request.method == "POST":
        categoryname = request.POST.get('categoryname')
        Category.objects.create(categoryname=categoryname)
        return redirect('manage_categories')  # Redirect to manage view after registration

    return render(request, 'register_category.html')  # Render registration form

# Search categories
def search_categories(request):
    query = request.GET.get('q', '')
    results = Category.objects.all()

    if query:
        results = results.filter(Q(categoryname__icontains=query))

    return render(request, 'search_category.html', {'results': results, 'query': query})

# Manage categories
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})
