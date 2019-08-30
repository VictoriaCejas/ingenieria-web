from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Usuario, TiposUsuario, EstadosUsuario
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


@login_required(login_url="login")
def Perfil(request):
    try:
        user = request.user
        tipo = Usuario.objects.get(usuario=user).tipo.idTipoUsuario
    except:
        tipo = 2

    return render(request, 'beautycalendar/perfil.html', {'tipo': tipo})


'''
def Signup(request):
    import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.(request)
            if user:
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')

            user = form.save(commit=False)
            user.is_active = False
            user.first_name = nombre
            user.last_name = apellido
            user.save()

            to_email = form.cleaned_data.get('email')

            correo = to_email

            estado = EstadosUsuario.objects.get(
                descripcion='pendiente activacion')
            tipoGet = form.cleaned_data.get('bussines')
            if tipoGet:
                tipo = TiposUsuario.objects.get(descripcion='bussines')
            else:
                tipo = TiposUsuario.objects.get(descripcion='cliente')

            usuario = Usuario(usuario=user, correo=correo, nombre=nombre,
                              apellido=apellido, estado=estado, tipo=tipo, reputacion=0)
            # guarda usuario
            usuario.save()

            return render(request, 'allauth/account/verification_sent.html', {})
           # return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SignupForm(data=request.POST)
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})
'''