from django.forms import ModelForm
from .models import Patient

class QuickPatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ["name", "age", "gender", "detail", "medicine_detail", "amount", "next_visit"]
