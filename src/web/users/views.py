from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.db import transaction
import logging
from django.core.paginator import Paginator
from .forms import UserForm
from .models import User
from web.appointments.models import Appointment

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm

    def get_success_url(self):
        success_url = self.request.GET.get('next') or reverse_lazy('index')
        logger.info(f"User {self.request.user} logged in successfully, redirecting to {
                    success_url}")
        return success_url

    def form_valid(self, form):
        logger.info(f"User {self.request.user} attempted to log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Login attempt failed for user {
                       self.request.POST.get('username')}.")
        return super().form_invalid(form)


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        return self.logout_user(request)

    def post(self, request, *args, **kwargs):
        return self.logout_user(request)

    def logout_user(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))


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
    if user.is_superuser or user.id == patient_id:
        return True
    if user.groups.filter(name='doctor').exists():
        return Appointment.objects.filter(doctor=user, patient_id=patient_id).exists()
    return False


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'users.view_user'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs.get('user_id')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user_type = self.kwargs.get('user_type')
        if not can_view_patient(request.user, self.user_id):
            raise PermissionDenied(
                "You do not have permission to view this user.")

        cache_key = f'user_detail_{self.user_id}'
        user = cache.get(cache_key)

        if not user:
            user = get_object_or_404(User, id=self.user_id)
            cache.set(cache_key, user, timeout=60*15)

        # Perform permission check
        if not can_view_patient(request.user, user_id):
            raise PermissionDenied(
                "You do not have permission to view this user.")

        # Get the user object
        user = get_object_or_404(User, id=user_id)

        # Render the response with the context data
        return render(request, 'users/user-detail.html', {'user': user, 'user_type': user_type})


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'users.delete_user'
    raise_exception = True

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['user_id'])

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to delete this user.")

        user.delete()
        user_type = self.kwargs.get('user_type')
        cache.delete(f'user_detail_{user.id}')
        return HttpResponseRedirect(reverse_lazy('manage-users', kwargs={'user_type': user_type}))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ManageUsersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'users/manage-users.html'
    context_object_name = 'users'
    permission_required = 'users.view_user'
    cache_timeout = 300
    paginate_by = 1

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        specialization_filter = self.request.GET.get('specialization', '')
        user_type = self.kwargs.get('user_type')

        cache_key = f"user_list_{self.request.user.id}_{
            user_type}_{search_query}_{specialization_filter}"

        # Check if the result is cached
        cached_users = cache.get(cache_key)
        if cached_users is not None:
            print("Returning cached users")
            return cached_users

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
                users = User.objects.filter(
                    doctor_appointment__doctor=self.request.user).distinct()
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
            raise PermissionDenied(
                "You do not have permission to view this page.")

        if search_query:
            users = users.filter(name__icontains=search_query)
        if specialization_filter:
            users = users.filter(specialization=specialization_filter)

        # Paginate the queryset
        paginator = Paginator(users, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Cache the paginated queryset
        cache.set(cache_key, page_obj, timeout=self.cache_timeout)

        return page_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.kwargs.get('user_type')
        context['search_query'] = self.request.GET.get('search', '')
        context['specializations'] = User.objects.values_list(
            'specialization', flat=True).distinct()
        context['specialization_filter'] = self.request.GET.get(
            'specialization', '')
        return context


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'users.delete_user'
    raise_exception = True

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['user_id'])

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if not request.user.is_superuser:
            raise PermissionDenied(
                "You do not have permission to delete this user.")

        # Wrap the delete operation in a transaction
        with transaction.atomic():
            user.delete()

        user_type = self.kwargs.get('user_type')
        return HttpResponseRedirect(reverse_lazy('manage-users', kwargs={'user_type': user_type}))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EditUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'users.change_user'
    raise_exception = True
    model = User
    form_class = UserForm
    template_name = 'users/edit-user.html'

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.kwargs['user_type']
        return context

    def form_valid(self, form):
        user = self.get_object()

        if not self.request.user.is_superuser and user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this user.")

        form.save()
        # Wrap the save operation in a transaction
        with transaction.atomic():
            form.save()

        user_type = self.kwargs.get('user_type')
        # Invalidate cache for the updated user
        cache.delete(f'user_detail_{user.id}')
        return redirect(reverse('manage-users', kwargs={'user_type': user_type}))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_type'] = self.kwargs.get('user_type')
        return kwargs


class CreateUserView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'users.create_user'
    raise_exception = True
    model = User
    form_class = UserForm
    template_name = 'users/add_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.kwargs['user_type']
        return context

    def form_valid(self, form):
        # Wrap the entire creation in a transaction
        with transaction.atomic():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()

            user_type = self.kwargs.get('user_type')

            if user_type == 'doctor':
                doctor_group, created = Group.objects.get_or_create(
                    name='doctor')
                user.groups.add(doctor_group)
            elif user_type == 'patient':
                patient_group, created = Group.objects.get_or_create(
                    name='patient')
                user.groups.add(patient_group)

        if user_type == 'doctor':
            doctor_group, created = Group.objects.get_or_create(name='doctor')
            user.groups.add(doctor_group)
        elif user_type == 'patient':
            patient_group, created = Group.objects.get_or_create(
                name='patient')
            user.groups.add(patient_group)
        # cache.delete(f'user_list_{user_type}')
        return redirect(reverse('manage-users', kwargs={'user_type': user_type}))
