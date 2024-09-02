from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def homepage_view(request):
    if request.user.is_superuser:
        return render(request, 'users/admin.html', {
            "Doctors": User.get_doctors()
        })
    else:
        return redirect('show_appointments')  # Replace with your actual homepage template

@login_required
def doctor_detail(request, doctor_id):
    if request.user.is_superuser:
        return render(request, 'users/doctor-detail.html', {
            'doctor': User.get_doctors().get(id=doctor_id)
        })
    return redirect('login')
