from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import QuickPatientForm

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
         return redirect('/')
      else:
         return redirect('doctor_login')
  
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
   return render(request,'doctor-dashboard.html')

#doctor and patient
def quick_add_patient(request):
   if request.method=='POST':
      form=QuickPatientForm(request.POST)
      if form.is_valid():
         form.save()
      else:
         messages.warning(request,"something went wrong!")
         return redirect('quick_add_patient')
   form=QuickPatientForm
   return render(request,'quick-add-patient-form.html',{
      'form':form
   })