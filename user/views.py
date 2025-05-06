from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Check if the user has a profile, create one if not
            try:
                profile = user.profile
            except:
                from .models import UserProfile
                UserProfile.objects.create(user=user)

            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def dashboard(request):
    from item.models import Item
    from django.db.models import Count

    # Get statistics
    total_items = Item.objects.count()
    claimed_items = Item.objects.filter(status='Claimed').count()
    unclaimed_items = Item.objects.filter(status='Unclaimed').count()

    # Calculate recovery rate
    recovery_rate = (claimed_items / total_items * 100) if total_items > 0 else 0
    recovery_rate = f"{recovery_rate:.2f}"  # Format to 2 decimal places

    # Get recent items
    recent_items = Item.objects.all().order_by('-date')[:5]

    context = {
        'user': request.user,
        'total_items': total_items,
        'claimed_items': claimed_items,
        'unclaimed_items': unclaimed_items,
        'recovery_rate': recovery_rate,
        'recent_items': recent_items,
    }

    return render(request, 'dashboard.html', context)

def welcome_view(request):
    return render(request, 'welcome.html')

def admin_required(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_required)
def list_users(request):
    users = User.objects.all()
    return render(request, 'admin.html', {'show_list': True, 'users': users})

@login_required
@user_passes_test(admin_required)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"User {user.username} updated successfully!")
            return redirect('list_users')
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)

    return render(request, 'update_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })

@login_required
@user_passes_test(admin_required)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully!")
        return redirect('list_users')
    return render(request, 'confirm_delete_user.html', {'user': user})

@login_required
@user_passes_test(admin_required)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was updated successfully!")
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
