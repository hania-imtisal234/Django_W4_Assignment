from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return render(request,'users/admin.html',{
                "Doctors":Doctor.objects.all()
                })
                else:
                    return redirect('home')  # Redirect to a non-admin home page
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def homepage_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'users/admin.html',{
        "Doctors":Doctor.objects.all()
        })
        else:
            return render(request, 'users/homepage.html')  # Replace with your actual homepage template
    else:
        return redirect('/login')  # Replace with your login URL
    
