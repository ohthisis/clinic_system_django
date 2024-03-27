from django.urls import path
from . import views

urlpatterns=[
    path('',views.doctor_login,name='doctor_login'),
    path('doctor/login/',views.doctor_login,name='doctor_login'),
    path('doctor/logout/',views.doctor_logout,name='doctor_logout'),
    path('doctor/reset-password/',views.doctor_reset_password,name='doctor_reset_password'),
    path('doctor/dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('doctor/quick-add-patient/',views.quick_add_patient,name='quick_add_patient'),
    path('patients',views.All_patients,name='all_patients'),
    path('patients/add',views.add_patient,name='add_patient'),
    path('patients/update/<int:id>',views.update_patient,name='update_patient'),
    path('patients/delete/<int:id>',views.delete_patient,name='delete_patient'),

    path('patients/email_template',views.email_template,name='email_template'),

    path('patients/n_patients',views.n_patients,name='n_patients'),
    # path('patients/patient_count_reports',views.patient_count_reports,name='patient_count_reports'),

    path('reports',views.reports,name='reports'),
    path('collection-report',views.collection_reports,name='collection_reports'),
    path('patients/add-visit/<int:patient_id>',views.add_visit,name='add_visit'),

]