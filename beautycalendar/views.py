from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Usuario, TiposUsuario, EstadosUsuario
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.


def Home(request):
    return render(request, 'beautycalendar/home.html', {})


def IniciarSesion(request):
    next = ""
    form = LoginForm(request.POST or None)
    if request.GET:
        next = request.GET['next']
    if request.method == 'POST' and form.is_valid():
        #next= request.POST['next']
        user = form.login(request)
        if user:
            login(request, user)
            next = request.POST.get('next', '/')
            if next == "accounts/login/":
                return redirect ('home')
            else:
                return HttpResponseRedirect(next)
        #  form = AuthenticationForm(data=request.POST)
        # if form.is_valid():
         #   user=form.get_user()
          #  login(request, user)
           # next = request.POST.get('next', '/')
            # return HttpResponseRedirect(next)
           # return HttpResponse(next)
    else:
        form = AuthenticationForm(data=request.POST)

    return render(request, "registration/login.html", {'form': form})


def CerrarSesion(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/accounts/login/')
def Private(request):
    return render(request, 'beautycalendar/privado.html', {})


def Public(request):
    return render(request, 'beautycalendar/publico.html', {})


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
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

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta.'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/activation_mail_send.html', {})
           # return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SignupForm(data=request.POST)
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})


def Activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        estadoActivado = EstadosUsuario.objects.get(descripcion='activo')
        usuario = Usuario.objects.get(usuario=user)
        usuario.estado = estadoActivado
        # Guarda usuario como activo
        usuario.save()
        #login(request, user)
        # return redirect('home')
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'registration/activation_complete.html', {})
       # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return render(request, 'registration/activate.html', {})
      #  return HttpResponse('Activation link is invalid!')


@login_required(login_url='/accounts/login/')
def Perfil(request):
    try:
        user = request.user
        tipo = Usuario.objects.get(usuario=user).tipo.idTipoUsuario
    except:
        tipo = 2

    return render(request, 'beautycalendar/perfil.html', {'tipo': tipo})


