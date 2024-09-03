from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.models import Group
from .forms import LoginForm, UserForm
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
        url = reverse('manage-users', kwargs={'user_type': 'doctor'})
        # Redirect to the generated URL
        return redirect(url)
    else:
        user_type = request.user.groups.values_list('name', flat=True).first()
        return redirect(reverse('show_appointments',kwargs={'user_id':request.user.id,'user_type':user_type}))  # Replace with your actual homepage template

@login_required
def user_detail(request,user_id,user_type):
    if request.user.is_superuser:
        return render(request, 'users/user-detail.html', {
            'user': User.get_by_id(user_id),
            'user_type':user_type
        })
    return redirect('login')

@login_required
def delete_user(request,user_id,user_type):
    if request.user.is_superuser:
        User.get_by_id(user_id).delete()
        return redirect('index')

@login_required
def manage_users(request, user_type):
    print(user_type)
    if user_type == 'doctor':
        users = User.get_doctors()
    elif user_type == 'patient':
        users = User.get_patients()
    else:
        users = []

    return render(request, 'users/manage-users.html', {'users': users, 'user_type': user_type})

def edit_user(request,user_type ,user_id):
    user=User.get_by_id(user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Replace with your actual URL name
    else:
        form = UserForm(instance=user, user=request.user)

    context = {
        'form': form,
        'user': user,
        'user_type': user_type,
    }

    return render(request,'users/edit-user.html',context)

def add_user(request, user_type):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user_type == 'doctor':
                doctor_group, created = Group.objects.get_or_create(name='doctor')
                user.groups.add(doctor_group)
            elif user_type == 'patient':
                patient_group, created = Group.objects.get_or_create(name='patient')
                user.groups.add(patient_group)
            else:
                # Handle other user types if necessary
                pass

            user.save()
            return redirect(reverse('manage-users', kwargs={'user_type': user_type}))
    else:
        form = UserForm()

    return render(request, 'users/add_user.html', {'form': form, 'user_type': user_type})

