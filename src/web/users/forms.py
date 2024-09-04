from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Name')
    phone_number = forms.CharField(label='Phone Number')
    address=forms.CharField(label='Address')
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


    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class UserForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        required=False
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        required=False
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Select gender'})
    )

    class Meta:
        model = User
        fields = [
            'username', 'name', 'email', 'phone_number', 'date_of_birth', 'gender', 'specialization', 'address'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'specialization': forms.TextInput(attrs={'placeholder': 'Enter specialization'})
        }

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super(UserForm, self).__init__(*args, **kwargs)
        if user_type != 'doctor':
            self.fields.pop('specialization', None)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if self.instance.pk:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                self.add_error('username', "Username already exists.")
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                self.add_error('email', "Email already exists.")
        else:
            if User.objects.filter(username=username).exists():
                self.add_error('username', "Username already exists.")
            if User.objects.filter(email=email).exists():
                self.add_error('email', "Email already exists.")

        return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
