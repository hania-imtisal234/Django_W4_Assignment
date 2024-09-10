from django import forms
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import Group
from .forms import UserForm
from .models import User
from web.appointments.models import Appointment
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
import logging






class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # The path to your login template
    redirect_authenticated_user = True  # Redirect if user is already logged in
    authentication_form = AuthenticationForm  # This is optional if you're using the default form
    print('Login 100')

    # @method_decorator(sensitive_post_parameters('password'))
    # @method_decorator(csrf_protect)
    # @method_decorator(never_cache)
    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('index')

def login_view(request):
    pass
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect('index')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})

# class CustomLogoutView(View):
#     def get(self, request, *args, **kwargs):
#         # Perform logout
#         logout(request)
#         return redirect(reverse_lazy('login'))
#
#     def post(self, request, *args, **kwargs):
#         # Perform logout
#         logout(request)
#         return redirect(reverse_lazy('login'))

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        return self.logout_user(request)

    def post(self, request, *args, **kwargs):
        return self.logout_user(request)

    def logout_user(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))

def logout_view(request):
    pass
    # logout(request)
    # return redirect('login')

# index view
@login_required
def homepage_view(request):
    pass
#     user_type = request.user.groups.values_list('name', flat=True).first()
#     if request.user.is_superuser:
#         return redirect('manage-users', user_type='doctor')
#     elif user_type:
#         return redirect('show_appointments', user_id=request.user.id, user_type=user_type)
#     else:
#         raise PermissionDenied("You do not have access to this page.")

logger = logging.getLogger(__name__)


class HomePageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_type = request.user.groups.values_list('name', flat=True).first()
        logger.debug(f"User Type: {user_type}")

        if request.user.is_superuser:
            return redirect('manage-users', user_type='doctor')
        elif user_type:
            return redirect('show_appointments', user_id=request.user.id, user_type=user_type)
        else:
            return self.handle_no_access()

    def handle_no_access(self):
        logger.warning("User does not have access.")
        raise PermissionDenied("You do not have access to this page.")

def can_view_patient(user, patient_id):
    if user.is_superuser:
        return True
    if user.id == patient_id:
        return True
    if user.groups.filter(name='doctor').exists():
        return Appointment.objects.filter(doctor=user, patient_id=patient_id).exists()
    return False

@login_required
@permission_required('users.view_user', raise_exception=True)
def user_detail(request, user_id, user_type):
    pass
    # user = get_object_or_404(User, id=user_id)
    #
    # @user_passes_test(lambda u: can_view_patient(u, user_id), login_url='login', redirect_field_name='index')
    # def inner_view(request):
    #     return render(request, 'users/user-detail.html', {'user': user, 'user_type': user_type})
    #
    # return inner_view(request)


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'users.view_user'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        # Use user_passes_test within the dispatch method, dynamically passing user_id
        user_id = self.kwargs.get('user_id')
        self.user_id = user_id
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user_type = self.kwargs.get('user_type')

        # Perform permission check
        if not can_view_patient(request.user, user_id):
            raise PermissionDenied("You do not have permission to view this user.")

        # Get the user object
        user = get_object_or_404(User, id=user_id)

        # Render the response with the context data
        return render(request, 'users/user-detail.html', {'user': user, 'user_type': user_type})


@login_required
@permission_required('users.delete_user', raise_exception=True)
def delete_user(request, user_id, user_type):
    pass
    # if request.user.is_superuser:
    #     user = get_object_or_404(User, id=user_id)
    #     user.delete()
    #     return redirect('manage-users', user_type=user_type)
    # else:
    #     raise PermissionDenied("You do not have permission to delete this user.")


# class DeleteUserView(LoginRequiredMixin, View):
#     permission_required = 'users.delete_user'
#     raise_exception = True
#
#     # @method_decorator(permission_required('users.delete_user', raise_exception=True))
#     def dispatch(self, request, *args, **kwargs):
#         self.user_id = kwargs.get('user_id')
#         self.user_type = kwargs.get('user_type')
#
#         if not request.user.is_superuser:
#             raise PermissionDenied("You do not have permission to delete this user.")
#
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         user = get_object_or_404(User, id=self.user_id)
#         user.delete()
#         return redirect('manage-users', user_type=self.user_type)

class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'users.delete_user'
    raise_exception = True

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['user_id'])

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to delete this user.")

        user.delete()
        user_type = self.kwargs.get('user_type')
        return HttpResponseRedirect(reverse_lazy('manage-users', kwargs={'user_type': user_type}))

    def get(self, request, *args, **kwargs):
        # If you don't want any confirmation page, redirect to the delete logic directly.
        return self.post(request, *args, **kwargs)

@login_required
@permission_required('users.view_user', raise_exception=True)
def manage_users(request, user_type):
    # pass
    search_query = request.GET.get('search', '')
    specialization_filter = request.GET.get('specialization', '')

    if search_query:
        specialization_filter = ''
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
        elif user_type == 'doctor':
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

    if search_query:
        users = users.filter(name__icontains=search_query)
    if specialization_filter:
        users = users.filter(specialization=specialization_filter)
    print(users)

    specializations = User.objects.values_list('specialization', flat=True).distinct()

    return render(request, 'users/manage-users.html', {
        'users': users,
        'user_type': user_type,
        'search_query': search_query,
        'specializations': specializations,
        'specialization_filter': specialization_filter
    })


class ManageUsersView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = User
    template_name = 'users/manage-users.html'  # Replace with your template
    context_object_name = 'users'
    permission_required = 'users.view_user'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        specialization_filter = self.request.GET.get('specialization', '')
        user_type = self.kwargs.get('user_type')

        if search_query:
            specialization_filter = ''
        if self.request.user.is_superuser:
            if user_type == 'doctor':
                users = User.get_doctors()
            elif user_type == 'patient':
                users = User.get_patients()
            else:
                raise ValidationError("Invalid user type specified.")
        elif self.request.user.groups.filter(name='doctor').exists():
            if user_type == 'patient':
                users = User.objects.filter(doctor_appointment__doctor=self.request.user).distinct()
            elif user_type == 'doctor':
                users = [self.request.user]
            else:
                raise ValidationError("Invalid user type specified.")
        elif self.request.user.groups.filter(name='patient').exists():
            if user_type == 'patient':
                users = [self.request.user]
            else:
                raise ValidationError("Invalid user type specified.")
        else:
            raise PermissionDenied("You do not have permission to view this page.")

        if search_query:
            users = users.filter(name__icontains=search_query)
        if specialization_filter:
            users = users.filter(specialization=specialization_filter)
        print(users)
        return users
        # specializations = User.objects.values_list('specialization', flat=True).distinct()



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.get_queryset()
        context['user_type'] = self.kwargs.get('user_type')
        context['search_query'] = self.request.GET.get('search', '')
        context['specializations'] = User.objects.values_list('specialization', flat=True).distinct()
        context['specialization_filter'] = self.request.GET.get('specialization', '')
        return context


@login_required
@permission_required('users.change_user', raise_exception=True)
def edit_user(request, user_type, user_id):
    pass
    # user = get_object_or_404(User, id=user_id)
    # if not request.user.is_superuser and user != request.user:
    #     raise PermissionDenied("You do not have permission to edit this user.")
    #
    # if request.method == 'POST':
    #     form = UserForm(request.POST, instance=user,user_type=user_type)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse('manage-users', kwargs={'user_type': user_type}))
    # else:
    #     form = UserForm(instance=user,user_type=user_type)
    #
    # return render(request, 'users/edit-user.html', {'form': form, 'user': user, 'user_type': user_type})

class EditUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'users.change_user'
    raise_exception = True
    model = User
    form_class = UserForm
    template_name = 'users/edit-user.html'

    def get_object(self):
        user_id = self.kwargs['user_id']
        return get_object_or_404(User, id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.kwargs['user_type']
        context['user'] = self.get_object()
        return context

    def form_valid(self, form):
        # Ensure that the user has permissions to edit
        user = self.get_object()

        # Prevent non-superusers from editing other users
        if not self.request.user.is_superuser and user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this user.")

        # Save the form if valid
        form.save()

        # Redirect to 'manage-users' view with user_type in URL
        user_type = self.kwargs.get('user_type')
        return redirect(reverse('manage-users', kwargs={'user_type': user_type}))

    def get_form_kwargs(self):
        # Add user_type to form instance
        kwargs = super().get_form_kwargs()
        kwargs['user_type'] = self.kwargs.get('user_type')
        return kwargs


@login_required
@permission_required('users.add_user', raise_exception=True)
def add_user(request, user_type):
    pass
    # print(user_type)
    # if request.method == 'POST':
    #     form = UserForm(request.POST, user_type=user_type)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.set_password(form.cleaned_data['password2'])
    #         user.save()
    #
    #         if user_type == 'doctor':
    #             doctor_group, created = Group.objects.get_or_create(name='doctor')
    #             user.groups.add(doctor_group)
    #         elif user_type == 'patient':
    #             patient_group, created = Group.objects.get_or_create(name='patient')
    #             user.groups.add(patient_group)
    #         return redirect(reverse('manage-users', kwargs={'user_type': user_type}))
    # else:
    #     form = UserForm(user_type=user_type)
    # return render(request, 'users/add_user.html', {'form': form, 'user_type': user_type})

class CreateUserView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'users.create_user'
    raise_exception = True
    model = User
    form_class = UserForm
    template_name = 'users/add_user.html'

    # def get_success_url(self):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.kwargs['user_type']
        # context['user'] = self.get_object()
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password2'])
        user.save()
        user_type = self.kwargs.get('user_type')

        if user_type == 'doctor':
            doctor_group, created = Group.objects.get_or_create(name='doctor')
            user.groups.add(doctor_group)
        elif user_type == 'patient':
            patient_group, created = Group.objects.get_or_create(name='patient')
            user.groups.add(patient_group)
        return redirect(reverse('manage-users', kwargs={'user_type': user_type}))

#There is no need to implement transaction in this file