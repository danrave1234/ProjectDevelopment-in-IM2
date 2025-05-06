from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True, label="Full Name")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Update the user's profile
            user.profile.full_name = self.cleaned_data['full_name']
            user.profile.phone_number = self.cleaned_data['phone_number']
            user.profile.save()

        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number']

class CustomUserChangeForm(UserChangeForm):
    full_name = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['full_name'].initial = self.instance.profile.full_name
            self.fields['phone_number'].initial = self.instance.profile.phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update the user's profile
            user.profile.full_name = self.cleaned_data['full_name']
            user.profile.phone_number = self.cleaned_data['phone_number']
            user.profile.save()
        return user
