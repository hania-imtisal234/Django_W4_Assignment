from django.contrib.auth import login, logout
from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied,ValidationError
from .forms import UserForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def homepage_view(request):
    user_type = request.user.groups.values_list('name', flat=True).first()
    if request.user.is_superuser:
        return redirect('manage-users', user_type='doctor')
    elif user_type:
        return redirect('show_appointments', user_id=request.user.id, user_type=user_type)
    else:
        raise PermissionDenied("You do not have access to this page.")

@login_required
@permission_required('users.view_user', raise_exception=True)
def user_detail(request, user_id, user_type):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_superuser or request.user == user:
        return render(request, 'users/user-detail.html', {'user': user, 'user_type': user_type})
    elif request.user.groups.filter(name='doctor').exists() and user.groups.filter(name='patient').exists() and user in request.user.doctor_appointment.all().values_list('patient', flat=True):
        # Doctor can view their own patients
        return render(request, 'users/user-detail.html', {'user': user, 'user_type': user_type})
    else:
        raise PermissionDenied("You do not have permission to view this user.")

@login_required
@permission_required('users.delete_user', raise_exception=True)
def delete_user(request, user_id, user_type):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('manage-users', user_type=user_type)
    else:
        raise PermissionDenied("You do not have permission to delete this user.")

@login_required
@permission_required('users.view_user', raise_exception=True)
def manage_users(request, user_type):
    if request.user.is_superuser:
        if user_type == 'doctor':
            users = User.get_doctors()
        elif user_type == 'patient':
            users = User.get_patients()
        else:
            raise ValidationError("Invalid user type specified.")
    elif request.user.groups.filter(name='doctor').exists():
        if user_type == 'patient':
            users = User.objects.filter(doctor_appointment__doctor=request.user).distinct()
        elif user_type == 'doctor' and request.user.groups.filter(name='doctor').exists():
            users = [request.user]
        else:
            raise ValidationError("Invalid user type specified.")
    elif request.user.groups.filter(name='patient').exists():
        if user_type == 'patient':
            users = [request.user]
        else:
            raise ValidationError("Invalid user type specified.")
    else:
        raise PermissionDenied("You do not have permission to view this page.")

    return render(request, 'users/manage-users.html', {'users': users, 'user_type': user_type})

@login_required
@permission_required('users.change_user', raise_exception=True)
def edit_user(request, user_type, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_superuser and user != request.user:
        raise PermissionDenied("You do not have permission to edit this user.")

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('manage-users', kwargs={'user_type': user_type}))
        else:
            raise ValidationError("Error in form submission.")
    else:
        form = UserForm(instance=user, user=request.user)

    return render(request, 'users/edit-user.html', {'form': form, 'user': user, 'user_type': user_type})

@login_required
@permission_required('users.add_user', raise_exception=True)
def add_user(request, user_type):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            if user_type == 'doctor':
                doctor_group, created = Group.objects.get_or_create(name='doctor')
                user.groups.add(doctor_group)
            elif user_type == 'patient':
                patient_group, created = Group.objects.get_or_create(name='patient')
                user.groups.add(patient_group)
            return redirect(reverse('manage-users', kwargs={'user_type': user_type}))
        else:
            raise ValidationError("Error in form submission.")
    else:
        form = UserForm()

    return render(request, 'users/add_user.html', {'form': form, 'user_type': user_type})
