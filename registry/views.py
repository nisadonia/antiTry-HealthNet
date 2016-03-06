from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User as DjangoUser
from .forms import PatientRegisterForm, LoginForm, AppointmentSchedulingForm
from .models.user_models import Patient
from .models.info_models import Appointment
# Create your views here.


def register(request):
    if request.method == "POST":
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            username = '%s%s%s' % (patient.first_name, patient.middle_initial, patient.last_name)
            patient.auth_user = DjangoUser.objects.create_user(username, form.cleaned_data['email'],
                                                         form.cleaned_data['password'])
            patient.save()
            return redirect('registry:index')
    else:
        form = PatientRegisterForm()
    return render(request, 'registry/new.html', {'form': form})

@login_required(login_url='/login')
def apptSchedule(request):
    if request.method == "POST":
        form = AppointmentSchedulingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('registry:index')
    else:
        form = AppointmentSchedulingForm()
    return render(request, 'registry/appointment.html', {'form': form})

def detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'registry/patient.html', {'patient': patient})


def index(request):
    return render(request,'registry/landing.html')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect(to='/login')
    else:
        form = LoginForm()
    return render(request, 'registry/login.html', {'form' : form})

def patient(request):
    return render(request, 'registry/patient.html')

def doc_nurse(request):
    return render(request, 'registry/doc_nurse.html')

def admins (request):
    return render(request, 'registry/admins.html')
