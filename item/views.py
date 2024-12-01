from django.core.paginator import Paginator
from django.db.models import Model, Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json, csv
from . import models
from .models import Item

def dashboard(request):
    if 'generate_report' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Category', 'Item Name', 'Description', 'Location', 'Status', 'Date Found'])
        for item in Item.objects.all():
            writer.writerow([
                item.categoryid.categoryname,
                item.itemname,
                item.itemdescription,
                f"{item.locationid.building} - Floor {item.locationid.floor}",
                item.status,
                item.date
            ])

        return response

    total_items = Item.objects.count()
    claimed_items = Item.objects.filter(status='Claimed').count()
    unclaimed_items = Item.objects.filter(status='Unclaimed').count()
    category_stats = list(Item.objects.values('categoryid__categoryname').annotate(count=Count('categoryid')).order_by('-count'))
    location_stats = list(Item.objects.values('locationid__building').annotate(count=Count('locationid')).order_by('-count'))

    # Calculate recovery rate
    recovery_rate = (claimed_items / total_items * 100) if total_items > 0 else 0
    recovery_rate = f"{recovery_rate:.2f}"  # Format to 2 decimal places

    context = {
        'total_items': total_items,
        'claimed_items': claimed_items,
        'unclaimed_items': unclaimed_items,
        'category_stats': json.dumps(category_stats),  # Serialize to JSON
        'location_stats': json.dumps(location_stats),  # Serialize to JSON
        'recovery_rate': recovery_rate,
    }
    return render(request, 'dashboard.html', context)

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
    date_query = request.GET.get('date', '')
    results = Item.objects.all()

    if query:
        results = results.filter(
            Q(itemname__icontains=query) |
            Q(itemdescription__icontains=query) |
            Q(categoryid__categoryname__icontains=query) |
            Q(locationid__building__icontains=query)
        )

    if date_query:
        results = results.filter(date=date_query)

    return render(request, 'search_results.html', {'results': results, 'query': query, 'date_query': date_query})

@csrf_exempt
def inventory_management(request):
    query = request.GET.get('q', '')
    date_query = request.GET.get('date', '')
    sort = request.GET.get('sort', '')
    page_number = request.GET.get('page', 1)

    items = Item.objects.all()

    if query:
        items = items.filter(
            Q(itemname__icontains=query) |
            Q(itemdescription__icontains=query) |
            Q(categoryid__categoryname__icontains=query) |
            Q(locationid__building__icontains=query)
        )

    if date_query:
        items = items.filter(date=date_query)

    if sort == 'Claimed':
        items = items.filter(status='Claimed')
    elif sort == 'Unclaimed':
        items = items.filter(status='Unclaimed')
    elif sort == 'recent':
        items = items.order_by('-date')
    elif sort == 'oldest':
        items = items.order_by('date')

    paginator = Paginator(items, 10)
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get('itemid')
        action = data.get('action')
        item = get_object_or_404(Item, pk=item_id)
        if action == 'Claim':
            item.status = 'Claimed'
        elif action == 'Unclaim':
            item.status = 'Unclaimed'
        item.save(update_fields=['status'])
        return JsonResponse({'success': True})

    return render(request, 'inventory_management.html', {'page_obj': page_obj, 'query': query, 'date_query': date_query, 'sort': sort})

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
    return render(request, 'confirm_delete.html', {'item': item})
