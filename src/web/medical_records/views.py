from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from web.medical_records.mixin import PermissionAndObjectMixin
from .models import MedicalRecord
from .forms import MedicalRecordForm
from web.appointments.models import Appointment


class MedicalRecordDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'medical_records/medical_record_detail.html'
    context_object_name = 'medical_record'
    permission_required = 'medical_records.view_medicalrecord'

    def get_object(self, queryset=None):
        return super().get_object(queryset=MedicalRecord.objects.select_related('patient', 'doctor', 'appointment'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medical_record = self.get_object()
        patient = medical_record.patient
        doctor = medical_record.doctor

        if not self.request.user.is_superuser and self.request.user != patient and self.request.user != doctor and not self.request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to view this medical record.")

        context.update({
            'patient': patient,
            'doctor': doctor,
        })
        return context


class PatientRecordDetailView(PermissionAndObjectMixin, DetailView):
    model = Appointment
    template_name = 'medical_records/medical_record_list.html'
    context_object_name = 'appointment'

    def get_object(self, queryset=None):
        return self.get_appointment()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()

        medical_records = MedicalRecord.objects.filter(
            patient=appointment.patient,
            doctor=appointment.doctor,
            appointment=appointment
        ).select_related('patient', 'doctor').order_by('-created_at')

        user_type = 'patient' if self.request.user == appointment.patient else 'doctor'
        user_id = appointment.patient.id if self.request.user == appointment.patient else appointment.doctor.id

        context.update({
            'medical_records': medical_records,
            'patient': appointment.patient,
            'doctor': appointment.doctor,
            'user_type': user_type,
            'user_id': user_id,
        })
        return context


class AddMedicalRecordView(LoginRequiredMixin, PermissionRequiredMixin, PermissionAndObjectMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/add_medical_record.html'
    permission_required = 'medical_records.add_medicalrecord'
    raise_exception = True

    def get_initial(self):
        initial = super().get_initial()
        patient, doctor = self.get_patient_and_doctor()
        appointment = self.get_appointment()

        initial.update({
            'patient': patient,
            'doctor': doctor,
            'appointment': appointment
        })
        return initial

    def form_valid(self, form):
        form.instance.patient = self.get_initial()['patient']
        form.instance.doctor = self.get_initial()['doctor']
        form.instance.appointment = self.get_initial()['appointment']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_initial())
        return context


class EditMedicalRecordView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/edit_medical_record.html'
    permission_required = 'medical_records.change_medicalrecord'
    raise_exception = True

    def get_object(self, queryset=None):
        record = super().get_object(queryset=MedicalRecord.objects.select_related(
            'patient', 'doctor', 'appointment'))
        if not self.request.user.is_superuser and not (
            self.request.user == record.doctor or
            self.request.user.is_staff
        ):
            raise PermissionDenied(
                "You do not have permission to edit this medical record.")

        return record

    def get_success_url(self):
        record = self.get_object()
        return reverse_lazy('patient_records', kwargs={
            'patient_id': record.patient.id,
            'doctor_id': record.doctor.id,
            'scheduled_at': int(record.appointment.scheduled_at.timestamp())
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medical_record'] = self.get_object()
        return context
