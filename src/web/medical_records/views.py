from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord
from .forms import MedicalRecordForm
from web.users.models import User
from web.appointments.models import Appointment

@login_required
def patient_records(request, patient_id, doctor_id,user_type):
    patient = User.get_by_id(patient_id)
    doctor = User.get_by_id(doctor_id)

    appointment = get_object_or_404(Appointment, patient=patient, doctor=doctor)

    medical_records = MedicalRecord.objects.filter(
        patient=patient,
        doctor=doctor,
        appointment=appointment
    ).order_by('-created_at')

    return render(request, 'medical_records/medical_record_list.html', {
        'user_type':user_type,
        'patient': patient,
        'medical_records': medical_records,
        'doctor': doctor,
        'appointment': appointment
    })

@login_required
def add_medical_record(request, patient_id, user_type):
    patient = get_object_or_404(User, id=patient_id)
    doctor = get_object_or_404(User, id=request.user.id)
    appointment = get_object_or_404(Appointment, patient=patient, doctor=doctor)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.doctor = doctor
            medical_record.appointment = appointment
            medical_record.save()
            return redirect('patient_records', user_type=user_type, patient_id=patient.id, doctor_id=doctor.id)
    else:
        form = MedicalRecordForm()

    return render(request, 'medical_records/add_medical_record.html', {'form': form, 'patient': patient, 'doctor': doctor, 'user_type':user_type})


@login_required
def edit_medical_record(request, record_id, user_type):
    record = get_object_or_404(MedicalRecord, id=record_id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect('patient_records', user_type=user_type, patient_id=record.patient.id, doctor_id=record.doctor.id)
    else:
        form = MedicalRecordForm(instance=record)

    return render(request, 'medical_records/edit_medical_record.html', {
        'user_type': user_type,
        'form': form,
        'record': record
    })
