from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category  # Ensure you have this import for the Category model

# Test view for categories
def categories_test(request):
    return HttpResponse("<h1>Hello, this is the view for Categories</h1>")

# Register a new category
def register_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category')

        if category_name:  # Ensure the category name is not empty
            Category.objects.create(
                categoryname=category_name
            )
            return redirect('manage_categories') 
        else:
            error_message = "Category name cannot be empty."
            return render(request, 'register_category.html', {'error': error_message})

    return render(request, 'register_category.html')

# Search for categories
def search_categories(request):
    query = request.GET.get('q', '')
    results = Category.objects.all()

    if query:
        results = results.filter(
            Q(categoryname__icontains=query)
        )

    return render(request, 'search_category.html', {'results': results, 'query': query})

# Manage categories
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

# Update an existing category
def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('category')
        if category_name:  # Ensure the updated name is not empty
            category.categoryname = category_name
            category.save()
            return redirect('manage_categories')

    return render(request, 'update_category.html', {'category': category})

# Delete a category
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_categories')  # Redirect back to manage categories

    return render(request, 'confirm_delete_category.html', {'category': category})
