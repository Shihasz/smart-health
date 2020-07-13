from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from ..decorators import doctor_required
from ..forms import DoctorSignUpForm
from ..models import User, Doctor, Appointment


class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('doctors:dashboard')


@method_decorator([login_required, doctor_required], name='dispatch')
class DashBoardView(TemplateView):
    template_name = 'healthapp/doctors/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        return context

@login_required
@doctor_required
def app_list_view(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'healthapp/doctors/app_list.html', {'appointments': appointments})


@login_required
@doctor_required
def update_status_view(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.status = True
    appointment.save()
    return app_list_view(request)
