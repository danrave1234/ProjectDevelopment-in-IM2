from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Location

# Create your views here.

def locations_test(request):
    return HttpResponse("<h1>Hello, this is the views for Locations</h1>")

def register_location(request):
    if request.method == "POST":
        building = request.POST.get('building')
        floor = request.POST.get('floor')

        Location.objects.create(
            building=building,
            floor=floor
        )
        return redirect('manage_locations') 

    return render(request, 'register_location.html')

def search_locations(request):
    query = request.GET.get('q', '')
    results = Location.objects.all()

    if query:
        results = results.filter(
            Q(building__icontains=query) |
            Q(floor__icontains=query)
        )

    return render(request, 'search_results.html', {'results': results, 'query': query})

def manage_locations(request):
    locations = Location.objects.all()
    return render(request, 'manage_location.html', {'locations': locations})

def update_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    if request.method == 'POST':
        location.building = request.POST.get('building')
        location.floor = request.POST.get('floor')
        location.save()
        return redirect('manage_locations')

    return render(request, 'update_location.html', {'location': location})

def delete_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    if request.method == 'POST':
        location.delete()
        return redirect('manage_locations')

    return render(request, 'confirm_delete_location.html', {'location': location})
