from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .models import MedicalRecord
from .forms import MedicalRecordForm
from web.users.models import User
from web.appointments.models import Appointment

@login_required
@permission_required('medical_records.view_medicalrecord', raise_exception=True)
def patient_records(request, patient_id, doctor_id):
    patient = get_object_or_404(User, id=patient_id)
    doctor = get_object_or_404(User, id=doctor_id)

    if request.user != patient and request.user != doctor and not request.user.is_staff:
        raise PermissionDenied("You do not have permission to view these medical records.")

    appointment = get_object_or_404(Appointment, patient=patient, doctor=doctor)
    medical_records = MedicalRecord.objects.filter(
        patient=patient,
        doctor=doctor,
        appointment=appointment
    ).order_by('-created_at')

    user_type = 'patient' if request.user == patient else 'doctor'
    user_id = patient.id if request.user == patient else doctor.id

    return render(request, 'medical_records/medical_record_list.html', {
        'patient': patient,
        'medical_records': medical_records,
        'doctor': doctor,
        'appointment': appointment,
        'user_type': user_type,
        'user_id': user_id,
    })

@login_required
@permission_required('medical_records.add_medicalrecord', raise_exception=True)
def add_medical_record(request, patient_id):
    # Get the patient object
    patient = get_object_or_404(User, id=patient_id)

    # Determine if the user is a superuser or a doctor
    if request.user.is_superuser:
        # Superuser can view all appointments for the patient
        appointment = get_object_or_404(Appointment, patient=patient)
        doctor = appointment.doctor
    else:
        # Non-superusers must be doctors and can only add records for their own patients
        doctor = get_object_or_404(User, id=request.user.id)
        appointment = get_object_or_404(Appointment, patient=patient, doctor=doctor)

        # Ensure the logged-in user is indeed a doctor and has an appointment with the patient
        if not doctor.groups.filter(name='doctor').exists():
            raise PermissionDenied("You do not have permission to add medical records for this patient.")

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.doctor = doctor
            medical_record.appointment = appointment
            medical_record.save()
            return redirect('patient_records', patient_id=patient.id, doctor_id=doctor.id)
    else:
        form = MedicalRecordForm()

    return render(request, 'medical_records/add_medical_record.html', {
        'form': form,
        'patient': patient,
        'doctor': doctor
    })
@login_required
@permission_required('medical_records.change_medicalrecord', raise_exception=True)
def edit_medical_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)

    if request.user != record.doctor and not request.user.is_staff:
        raise PermissionDenied("You do not have permission to edit this medical record.")

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect('patient_records', patient_id=record.patient.id, doctor_id=record.doctor.id)
    else:
        form = MedicalRecordForm(instance=record)

    return render(request, 'medical_records/edit_medical_record.html', {
        'form': form,
        'record': record
    })


@login_required
@permission_required('medical_records.view_medicalrecord', raise_exception=True)
def medical_record_detail(request, record_id):
    # Fetch the medical record by ID
    medical_record = get_object_or_404(MedicalRecord, id=record_id)

    # Fetch the associated patient and doctor
    patient = medical_record.patient
    doctor = medical_record.doctor

    # Ensure that the current user is either the associated patient, doctor, or a staff member
    if request.user != patient and request.user != doctor and not request.user.is_staff:
        raise PermissionDenied("You do not have permission to view this medical record.")

    return render(request, 'medical_records/medical_record_detail.html', {
        'medical_record': medical_record,
        'patient': patient,
        'doctor': doctor,
    })
