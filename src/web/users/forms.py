from django.contrib.auth.forms import AuthenticationForm
# from .models import User, Doctor
#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
#
#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         username = cleaned_data.get('username')
#
#         if User.objects.filter(email=email).exists():
#             self.add_error('email', 'A user with this email already exists.')
#
#         if User.objects.filter(username=username).exists():
#             self.add_error('username', 'A user with this username already exists.')
#
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#             if user.role == 'doctor':
#                 Doctor.objects.create(user=user)
#         return user
#
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Name')
    phone_number = forms.CharField(label='Phone Number')
    date_of_birth = forms.DateField(label='Date of Birth', required=False, widget=forms.SelectDateWidget(years=range(1900, 2100)))
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female')], required=False)
    specialization = forms.CharField(label='Specialization', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'phone_number', 'date_of_birth', 'gender', 'specialization', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        return phone_number

    # The specialization clean method and logic related to 'doctor' group has been removed

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name', 'email', 'phone_number', 'date_of_birth', 'gender', 'specialization'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'specialization': forms.TextInput(attrs={'placeholder': 'Enter specialization'})
        }

    def __init__(self, *args, **kwargs):
        # Initialize form with user instance
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.groups.filter(name='doctor').exists():
            # Remove specialization field if user is not a doctor
            self.fields.pop('specialization')

