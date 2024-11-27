from django.db.models import Model, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from item.models import Item
from . import models


# TEST
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
        return redirect('manage_inventory')

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
            Q(categoryid__categoryname__icontains=query) |
            Q(date__icontains=query)
        )

    return render(request, 'search_results.html', {'results': results, 'query': query})


from django.shortcuts import render
from .models import Item  # assuming your model is named Item


def inventory_management(request):
    query = request.GET.get('q', '')  # Get the search query from the GET parameters
    sort = request.GET.get('sort', '')  # Get the sort parameter from the GET parameters

    if query:
        items = Item.objects.filter(
            Q(itemname__icontains=query) |
            Q(itemdescription__icontains=query) |
            Q(categoryid__categoryname__icontains=query) |
            Q(locationid__building__icontains=query)
        )
    else:
        items = Item.objects.all()  # Show all items if no search query

    if sort == 'claimed':
        items = items.filter(status='claimed')
    elif sort == 'unclaimed':
        items = items.filter(status='unclaimed')

    if request.method == "POST":
        item_id = request.POST.get('itemid')
        action = request.POST.get('action')
        item = get_object_or_404(Item, pk=item_id)
        if action == 'claim':
            item.status = 'claimed'
        elif action == 'unclaim':
            item.status = 'unclaimed'
        item.save(update_fields=['status'])
        return redirect('manage_inventory')

    return render(request, 'inventory_management.html', {'items': items})


def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == "POST":
        itemname = request.POST.get('itemname')
        itemdescription = request.POST.get('itemdescription')
        categoryid = request.POST.get('categoryid')  # This should not be empty
        locationid = request.POST.get('locationid')

        print(f"Item Name: {itemname}, Item Description: {itemdescription}, Category ID: {categoryid}, Location ID: {locationid}")

        if categoryid:  # Check if categoryid is not empty
            item.categoryid = models.Category.objects.get(pk=categoryid)
        else:
            return HttpResponse("Category ID cannot be empty!", status=400)

        if locationid:  # Check if locationid is not empty
            item.locationid = models.Location.objects.get(pk=locationid)

        item.itemname = itemname
        item.itemdescription = itemdescription
        item.save()
        return redirect('manage_inventory')

    categories = models.Category.objects.all()
    locations = models.Location.objects.all()
    return render(request, 'update_item.html', {'item': item, 'categories': categories, 'locations': locations})

def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        item.delete()
        return redirect('manage_inventory')
    return render(request, 'confirm_delete.html', {'item': item})  # Create a confirmation template if desired
