from dataclasses import fields
from rest_framework import serializers
from web.medical_records.models import MedicalRecord
from web.users.models import User
from web.appointments.models import Appointment


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ('id', 'patient', 'doctor', 'appointment', 'diagnosis',
                  'treatment', 'notes', 'report', 'created_at', 'updated_at')


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='doctor'))
    patient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='patient'))
    medical_record = MedicalRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'doctor', 'patient', 'scheduled_at',
                  'created_at', 'updated_at', 'medical_record')
