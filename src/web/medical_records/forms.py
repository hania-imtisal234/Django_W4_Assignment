# web/medical_records/forms.py
from django import forms
from .models import MedicalRecord

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment', 'notes', 'report']  # Exclude patient, doctor, and appointment as these are handled separately
