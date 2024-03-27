from django.forms import ModelForm
from .models import Patient,Visit
from django import forms

class QuickPatientForm(ModelForm):
    detail=forms.CharField(widget=forms.Textarea)
    medicine_detail=forms.CharField(widget=forms.Textarea)
    amount=forms.IntegerField()
    next_visit=forms.IntegerField()
    class Meta:
        model = Patient
        fields = ["name","age", "gender", "detail", "medicine_detail", "amount", "next_visit"]

    def __init__(self, *args, **kwargs):
        super(QuickPatientForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PatientForm(ModelForm):
    detail=forms.CharField(widget=forms.Textarea)
    medicine_detail=forms.CharField(widget=forms.Textarea)
    note=forms.CharField(widget=forms.Textarea)
    amount=forms.IntegerField()
    next_visit=forms.IntegerField()
    class Meta:
        model = Patient
        fields = ["name","email", "age", "gender", "detail", "medicine_detail","address","mobile","amount", "next_visit","note"]

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields["address"].required=False
        self.fields["address"].widget.attrs['rows']='5'
        self.fields["note"].widget.attrs['rows']='5'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class VisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = ["detail", "medicine_detail","amount", "next_visit","note"]

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        self.fields["note"].widget.attrs['rows']='5'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
