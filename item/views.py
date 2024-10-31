from django.db.models import Model, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from item.models import Item
from . import models

# Create your views here.

def items_test(request):
    return HttpResponse("<h1>Hello, this is the views for Items</h1>")

def register_item(request):
    if request.method == "POST":
        itemname = request.POST.get('itemname')
        itemdescription = request.POST.get('itemdescription')
        categoryid = request.POST.get('categoryid')
        locationid = request.POST.get('locationid')

        category = models.Category.objects.get(pk=categoryid)
        location = models.Location.objects.get(pk=locationid)

        Item.objects.create(
            itemname=itemname,
            itemdescription=itemdescription,
            date=timezone.now(),
            categoryid=category,
            locationid=location
        )
        return redirect('item_list')

    categories = models.Category.objects.all()
    locations = models.Location.objects.all()
    return render(request, 'register_item.html', {'categories': categories, 'locations': locations})

def search_items(request):
    query = request.GET.get('q', '')
    results = Item.objects.all()

    if query:
        results = results.filter(
            Q(itemname__icontains=query) |
            Q(itemdescription__icontains=query) |
            Q(categoryid__categoryName__icontains=query) |
            Q(date__icontains=query)
        )

    return render(request, 'search_results.html', {'results': results, 'query': query})


def manage_inventory(request):
    items = Item.objects.all()

    if request.method == "POST":
        itemid = request.POST.get("itemid")
        item = Item.objects.get(pk=itemid)
        item.status = "claimed" if item.status == "unclaimed" else "unclaimed"
        item.save()

    return render(request, 'inventory_management.html', {'items': items})
