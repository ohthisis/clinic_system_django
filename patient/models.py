from django.db import models
#from python
from datetime import date

GENDER_CHOICES=(
    ('male','Male'),
    ('female','Female'),
    ('other','Other'),
)

# Create your models here.
class Patient(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(null=True,blank=True)
    age=models.IntegerField(default=0)
    gender=models.CharField(choices=GENDER_CHOICES,default='male')
    mobile=models.IntegerField(null=True)
    address=models.TextField(null=True)
    detail=models.TextField(null=True)
    medicine_detail=models.TextField(null=True)
    note=models.TextField(null=True)
    amount=models.DecimalField(max_digits=10,decimal_places =2,default=0)
    next_visit=models.IntegerField(default=0)
    visit_date=models.DateField(default=date.today(),null=True)
    added_time=models.DateTimeField(auto_now_add=True,null=True)