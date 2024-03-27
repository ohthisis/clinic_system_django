from django.test import TestCase
from datetime import date,timedelta
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import Patient
# Create your tests here.
def send_next_visit_email_notification():
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
