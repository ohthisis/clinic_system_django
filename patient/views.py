from datetime import date,timedelta
import calendar

from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Count,Sum
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import transaction,IntegrityError

from .forms import VisitForm,VisitForm,QuickPatientForm
from .models import Visit,Visit
from django.urls import reverse_lazy
from .models import Patient


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
   totalPatients=Patient.objects.count()
   totalCollection=Visit.objects.aggregate(total=Sum('amount'))
   return render(request,'doctor-dashboard.html',
                 {'page_title':'Dashboard',
                 'totalPatients':totalPatients,
                 'totalCollection':totalCollection
                 }
                 )

#doctor and Visit
def quick_add_patient(request):
   if request.method=='POST':
      try:
         with transaction.atomic():
            form=QuickPatientForm(request.POST)
            if form.is_valid():
               Visit=form.save()
               visit=Visit.objects.create(
                  Visit=Visit,
                  detail=form.cleaned_data['detail'],
                  medicine_detail=form.cleaned_data['medicine_detail'],
                  next_visit=form.cleaned_data['next_visit'],
                  amount=form.cleaned_data['amount'],
               )
               messages.success(request,"Visit added successfully")
               return redirect('quick_add_patient')
            else:
               messages.warning(request,"Something went wrong!!")
               return redirect('quick_add_patient')
      except IntegrityError:
         messages.warning(request,"Something went wrong!!")
         return redirect('quick_add_patient')
   else:
      form=QuickPatientForm
      return render(request,'quick-add-patient-form.html',{
      'form':form
   })

def All_patients(request):
   data=Visit.objects.all().order_by('-id')
   return render(request,'all-patient.html',{'data':data})

#doctor add Visit
def add_patient(request):
   if request.method=='POST':
      form=VisitForm(request.POST)
      try:
         with transaction.atomic():
            if form.is_valid():
               Visit=form.save()
               visit=Visit.objects.create(
                  Visit=Visit,
                  detail=form.cleaned_data['detail'],
                  medicine_detail=form.cleaned_data['medicine_detail'],
                  next_visit=form.cleaned_data['next_visit'],
                  amount=form.cleaned_data['amount'],
                  note=form.cleaned_data['note'],
                  )
               messages.success(request,"Patient added successfully")
               return redirect('add_patient')
            else:
               print(form.errors)
               messages.warning(request,"something went wrong!")
               return redirect('add_patient')
      except IntegrityError:
         messages.warning(request,"Something went wrong!!")
         return redirect('add_patient')
   else:
      form=VisitForm
      return render(request,'add-patient-form.html',{
      'form':form
   })
#add visit Visit
def add_visit(request,Visit_id):
   if request.method=='POST':
      Visit=Visit.objects.get(id=Visit_id)
      form=VisitForm(request.POST)
      if form.is_valid():
         form.Visit=Visit
         visit=form.save(commit=False)
         visit.Visit=Visit         
         visit.save()
         messages.success(request,"Visit added successfully")
         return redirect(reverse_lazy('add_visit',kwargs={'Visit_id':Visit_id}))
      else:
         print(form.errors)
         messages.warning(request,"Somethings went wrong!!")
         return redirect(reverse_lazy('add_visit',kwargs={'Visit_id':Visit_id}))
      
   else:
      form=VisitForm
      return render(request,'visit-form.html',{
      'form':form,
      'page_title':'Add Visit'
   })  

def update_patient(request,id):
   Visit=Visit.objects.get(id=id)
   if request.method=='POST':
      form=VisitForm(request.POST,instance=Visit)
      if form.is_valid():
         form.save()
         messages.success(request,"Visit update successfully")
         return redirect('update_Visit',id)
      else:
         print(form.errors)
         messages.warning(request,"something went wrong!")
         return redirect('update_Visit',id)
   else:
      form=VisitForm(instance=Visit)
      return render(request,'update-Visit-form.html',{
      'form':form
   })

def delete_patient(request,id):
   Visit.objects.get(id=id).delete()
   messages.success(request,"Visit deleted successfully")
   return redirect('all_Visits')

def email_template(request):
   return render(request,'email_templates.html')

def n_patients(request):
   Visits=Visit.objects.filter(visit_date__lt=date.today())

   count=0
   for Visit in Visits:
      nextVisitDate=Visit.visit_date+timedelta(days=Visit.next_visit)
      notificationDate=nextVisitDate-timedelta(days=1)
      print("noti",notificationDate)
      print(date.today())
      if notificationDate == date.today():
         subject=f'Doctor next visit'
         msg=render_to_string('email_templates.html',{'next_visit':nextVisitDate,'Visit':Visit})
         email_form =settings.EMAIL_HOST_USER
         recipient_list=[Visit.email]
         mail=EmailMessage(subject,msg,email_form,recipient_list)
         mail.content_subtype="html"
         mail.send()
         count+=1
   return render(request,'n_Visit.html',{
      'Visits':Visits,
      'count':count
   })

def reports(request):
   selectedYear=date.today().year
   if request.GET.get('year'):
      selectedYear=request.GET.get('year')
   selectedMonth=date.today().month
   if request.GET.get('month'):
      selectedMonth=request.GET.get('month')

   #Fetch Year
   years=Visit.objects.values('visit_date__year').annotate(total=Count('id'))

    #Fetch Month
   monthNames=[]
   months=Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Count('id'))
   for month in months:
      monthNames.append({'id':month['visit_date__month'],'name':calendar.month_name[month['visit_date__month']]})
   #Chart By Dates 
   dVisits=Visit.objects.filter(visit_date__year=selectedYear,visit_date__month=selectedMonth).values('visit_date').annotate(total=Count('id'))

   dailyChartLabels=[]
   dailyChartValues=[]

   for data in dVisits:
         dailyChartLabels.append(data['visit_date'].strftime('%d-%m-%y'))
         dailyChartValues.append(data['total'])


   #Chart By Month
   mVisits=Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Count('id'))
   monthChartLabels=[] 
   monthChartValues=[]
   
   for data in mVisits:
      monthName=calendar.month_name[data['visit_date__month']]
      monthChartLabels.append(monthName)
      monthChartValues.append(data['total'])

   #Chart By Yearly
   yVisits=Visit.objects.values('visit_date__year').annotate(total=Count('id'))
   yearChartLabels=[] 
   yearChartValues=[]
   
   for data in yVisits:
      yearName=data['visit_date__year']
      yearChartLabels.append(yearName)
      yearChartValues.append(data['total'])

   return render(request,'reports.html',{
      'dailyVisits':dVisits,
      'page_Title':'Reports',
      'dailyChart':{
         'dailyChartLabels':dailyChartLabels,
         'dailyChartValues':dailyChartValues
         },
      'monthlyChart':{
         'monthlyChartLabels':monthChartLabels,
         'monthlyChartValues':monthChartValues
         },
            'yearlyChart':{
         'yearChartLabels':yearChartLabels,
         'yearChartValues':yearChartValues
         },
         'years':years,
         'currentYear':int(selectedYear),
         'currentMonth':int(selectedYear),
         'monthNames':monthNames

   })

# collection reports
def collection_reports(request):

   selectedYear=date.today().year
   if request.GET.get('year'):
      selectedYear=request.GET.get('year')
   selectedMonth=date.today().month
   if request.GET.get('month'):
      selectedMonth=request.GET.get('month')

   #Fetch Year
   years=Visit.objects.values('visit_date__year').annotate(total=Count('id'))

    #Fetch Month
   monthNames=[]
   months=Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Count('id'))
   for month in months:
      monthNames.append({'id':month['visit_date__month'],'name':calendar.month_name[month['visit_date__month']]})
   #Chart By Dates 
   dVisits=Visit.objects.filter(visit_date__year=selectedYear,visit_date__month=selectedMonth).values('visit_date').annotate(total=Sum('amount'))

   dailyChartLabels=[]
   dailyChartValues=[]

   for data in dVisits:
         dailyChartLabels.append(data['visit_date'].strftime('%d-%m-%y'))
         dailyChartValues.append(float(data['total']))


   #Chart By Month
   mVisits=Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Sum('amount'))
   monthChartLabels=[] 
   monthChartValues=[]
   
   for data in mVisits:
      monthName=calendar.month_name[data['visit_date__month']]
      monthChartLabels.append(monthName)
      monthChartValues.append(data['total'])

   #Chart By Yearly
   yVisits=Visit.objects.values('visit_date__year').annotate(total=Sum('amount'))
   yearChartLabels=[] 
   yearChartValues=[]
   
   for data in yVisits:
      yearName=data['visit_date__year']
      yearChartLabels.append(yearName)
      yearChartValues.append(data['total'])

   return render(request,'collection_report.html',{
      'dailyVisits':dVisits,
      'page_Title':'Reports',
      'dailyChart':{
         'dailyChartLabels':dailyChartLabels,
         'dailyChartValues':dailyChartValues
         },
      'monthlyChart':{
         'monthlyChartLabels':monthChartLabels,
         'monthlyChartValues':monthChartValues
         },
            'yearlyChart':{
         'yearChartLabels':yearChartLabels,
         'yearChartValues':yearChartValues
         },
         'years':years,
         'currentYear':int(selectedYear),
         'currentMonth':int(selectedYear),
         'monthNames':monthNames

   })