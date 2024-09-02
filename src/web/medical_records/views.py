from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord
from .forms import MedicalRecordForm
from web.users.models import User
from web.appointments.models import Appointment

@login_required
def patient_records(request, patient_id, doctor_id):
    patient = User.get_by_id(patient_id)
    doctor = User.get_by_id(doctor_id)

    appointment = get_object_or_404(Appointment, patient=patient, doctor=doctor)

    medical_records = MedicalRecord.objects.filter(
        patient=patient,
        doctor=doctor,
        appointment=appointment
    ).order_by('-created_at')

    return render(request, 'medical_records/medical_record_list.html', {
        'patient': patient,
        'medical_records': medical_records,
        'doctor': doctor,
        'appointment': appointment
    })
@login_required
def add_medical_record(request, patient_id):
    patient = User.get_by_id(patient_id)
    doctor = User.get_by_id(request.user.id)
    appointment = get_object_or_404(Appointment, patient=patient, doctor=doctor)

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

    return render(request, 'medical_records/add_medical_record.html', {'form': form, 'patient': patient, 'doctor': doctor})

@login_required
def edit_medical_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)

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
