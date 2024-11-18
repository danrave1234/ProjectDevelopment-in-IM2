from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category

def categories_test(request):
    return HttpResponse("<h1>Hello, this is the view for Categories</h1>")

def register_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category')

        if category_name:  
            Category.objects.create(
                categoryname=category_name
            )
            return redirect('manage_categories') 
        else:
            error_message = "Category name cannot be empty."
            return render(request, 'register_category.html', {'error': error_message})

    return render(request, 'register_category.html')

def search_categories(request):
    query = request.GET.get('q', '').strip()
    
    # If the query is empty, redirect to the manage_categories page
    if not query:
        return redirect('manage_categories')
    
    results = Category.objects.filter(categoryname__icontains=query)
    return render(request, 'manage_categories.html', {
        'categories': results,
        'query': query,
    })

def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('category')
        if category_name: 
            category.categoryname = category_name
            category.save()
            return redirect('manage_categories')

    return render(request, 'update_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        
        category.delete()
        return redirect('manage_categories')

    return render(request, 'confirm_delete_category.html', {'category': category})
