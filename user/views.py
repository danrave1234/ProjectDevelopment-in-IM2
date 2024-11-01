from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def user_test(request):
    return HttpResponse("<h1>Hello, this is the user test view.</h1>")

# Register
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inventory_management')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inventory_management')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user  
    return render(request, 'inventory_management.html', {'user': user})
