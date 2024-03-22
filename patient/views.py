from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Patient

from .forms import QuickPatientForm,PatientForm
#from python
from datetime import date,timedelta

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.
def home(request):
   return render(request,'home.html')

def doctor_login(request):
   if request.method=="POST":
      username = request.POST.get('username')
      password=request.POST.get('password')
      print(request.POST)
      user=authenticate(request,username=username,password=password)
      if user:
         login(request,user)
         return redirect('doctor_dashboard')
      else:
         messages.warning(request,"Invalid username/password!!")
  
   return render(request,'login.html',{
      'page_title':'Doctor login',
   })

def doctor_logout(request):
   logout(request)
   return redirect('doctor_login')

def doctor_reset_password(request):
   if not request.user.is_authenticated:
      return redirect('doctor_login')

   if request.method=="POST":
      password=request.POST.get('password')
      request.user.set_password(password)
      request.user.save()
      messages.success(request,"Password has been changed")
      return redirect('doctor_login')

      
   return render(request,'reset_password.html')

def doctor_dashboard(request):
   return render(request,'doctor-dashboard.html',{'page_title':'Dashboard'})

#doctor and patient
def quick_add_patient(request):
   if request.method=='POST':
      form=QuickPatientForm(request.POST)
      if form.is_valid():
         form.save()
         messages.success(request,"patient added successfully")
         return redirect('quick_add_patient')
      else:
         messages.warning(request,"something went wrong!")
         return redirect('quick_add_patient')
   else:
      form=QuickPatientForm
      return render(request,'quick-add-patient-form.html',{
      'form':form
   })

def All_patients(request):
   data=Patient.objects.all().order_by('-id')
   return render(request,'all-patient.html',{'data':data})

#doctor add patient
def add_patient(request):
   if request.method=='POST':
      form=PatientForm(request.POST)
      if form.is_valid():
         form.save()
         messages.success(request,"patient added successfully")
         return redirect('add_patient')
      else:
         print(form.errors)
         messages.warning(request,"something went wrong!")
         return redirect('add_patient')
   else:
      form=PatientForm
      return render(request,'add-patient-form.html',{
      'form':form
   })

def update_patient(request,id):
   patient=Patient.objects.get(id=id)
   if request.method=='POST':
      form=PatientForm(request.POST,instance=patient)
      if form.is_valid():
         form.save()
         messages.success(request,"patient update successfully")
         return redirect('update_patient',id)
      else:
         print(form.errors)
         messages.warning(request,"something went wrong!")
         return redirect('update_patient',id)
   else:
      form=PatientForm(instance=patient)
      return render(request,'update-patient-form.html',{
      'form':form
   })

def delete_patient(request,id):
   Patient.objects.get(id=id).delete()
   messages.success(request,"patient deleted successfully")
   return redirect('all_patients')

def email_template(request):
   return render(request,'email_templates.html')

def n_patients(request):
   patients=Patient.objects.filter(visit_date__lt=date.today())

   count=0
   for patient in patients:
      nextVisitDate=patient.visit_date+timedelta(days=patient.next_visit)
      notificationDate=nextVisitDate-timedelta(days=1)
      print("noti",notificationDate)
      print(date.today())
      if notificationDate == date.today():
         subject=f'Doctor next visit'
         msg=render_to_string('email_templates.html',{'next_visit':nextVisitDate,'patient':patient})
         email_form =settings.EMAIL_HOST_USER
         recipient_list=[patient.email]
         mail=EmailMessage(subject,msg,email_form,recipient_list)
         mail.content_subtype="html"
         mail.send()
         count+=1
   return render(request,'n_patient.html',{
      'patients':patients,
      'count':count
   })