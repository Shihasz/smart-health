from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, TemplateView

from ..decorators import patient_required
from ..forms import PatientSignUpForm, AppointmentForm
from ..models import User, Appointment, Patient


class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('patients:dashboard')


@method_decorator([login_required, patient_required], name='dispatch')
class DashboardView(TemplateView):
    template_name = 'healthapp/patients/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        return context


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'healthapp/patients/app_form.html'

    def form_valid(self, form):
        appointment = form.save()
        appointment.patient = Patient.objects.get(user=self.request.user)
        appointment.save()
        return redirect('patients:dashboard')

