from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomSignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from allauth.account.utils import send_email_confirmation

# Create your views here.


def Home(request):
    return render(request, 'beautycalendar/home.html', {})
 

@login_required(login_url='/accounts/login/')
def Private(request):
    return render(request, 'beautycalendar/privado.html', {})


def Public(request):
    return render(request, 'beautycalendar/publico.html', {})


@login_required
def Perfil(request):
    user= request.user
    usuario= Usuario.objects.get(usuario=user)
    tipo = Usuario.objects.get(usuario=user).tipo.idTipoUsuario


    return render(request, 'beautycalendar/perfil.html', {'usuario': usuario,'user':user,'tipo':tipo})


