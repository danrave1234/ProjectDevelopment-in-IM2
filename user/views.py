from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

def user_test(request):
    return HttpResponse("<h1>Hello, this is the user test view.</h1>")

# Register
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('manage_users')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('manage_users')
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
    return render(request, 'manage_users.html', {'user': request.user})
    # return redirect('manage_users')

# Admin check decorator
def admin_required(user):
    return user.is_superuser

# View to list all users
@login_required
#@user_passes_test(admin_required)
def list_users(request):
    users = User.objects.all()
    return render(request, 'admin.html', {'show_list': True, 'users': users})

# View to update user information
@login_required
#@user_passes_test(admin_required)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})

# View to delete a user
@login_required
#@user_passes_test(admin_required)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')
    return render(request, 'confirm_delete_user.html', {'user': user})

# Manage users
@login_required
# @user_passes_test(admin_required)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})
