from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Doctor

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'A user with this email already exists.')
        
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'A user with this username already exists.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.role == 'doctor':
                Doctor.objects.create(user=user)
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
