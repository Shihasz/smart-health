from django.urls import path, include
from django.contrib.auth import views as auth_views

from healthapp.views import predict, patients, doctors

urlpatterns = [
    path('', predict.index, name='index'),
    path('main/', predict.main_symptom, name='main'),
    path('related/', predict.process_symptoms, name='related'),
    path('result/', predict.result_view, name='result'),
    path('another/', predict.predict_another, name='another'),

    path('accounts/login', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/patient/', patients.PatientSignUpView.as_view(), name='patient_signup'),
    path('accounts/signup/doctor/', doctors.DoctorSignUpView.as_view(), name='doctor_signup'),

    path('patients/', include(([
                                   path('', patients.DashboardView.as_view(), name='dashboard'),
                                   path('app_form/', patients.AppointmentView.as_view(),
                                        name='app_form'),
                               ], 'hospital'), namespace='patients')),

    path('doctors/', include(([
                                   path('', doctors.DashBoardView.as_view(), name='dashboard'),
                                   path('app_list', doctors.app_list_view, name='app_list'),
                                   path('update_status/<int:pk>/',
                                        doctors.update_status_view, name='status_update'),
                                ], 'hospital'), namespace='doctors')),
]