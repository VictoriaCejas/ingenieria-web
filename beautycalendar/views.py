from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Usuario, TiposUsuario, EstadosUsuario
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.
def home(request):
    return render(request, 'beautycalendar/home.html', {})

def IniciarSesion(request):
    next=""
    if request.GET:
        next=request.GET['next']
    if request.method=='POST':
        #next= request.POST['next']
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
           # return HttpResponse(next)
    else:
        form = AuthenticationForm(data=request.POST)

    return render(request,"registration/login.html",{'form':form})

def CerrarSesion(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/accounts/login/')
def Private(request):
   return render(request,'beautycalendar/privado.html',{})

def Public(request):
   return render(request,'beautycalendar/publico.html',{})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():          
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            to_email = form.cleaned_data.get('email')
      
            correo=to_email
            nombre= form.cleaned_data.get('nombre')
            apellido= form.cleaned_data.get('apellido')
            estado= EstadosUsuario.objects.get(descripcion='pendiente activacion')
            tipo= TiposUsuario.objects.get(descripcion='cliente')
            usuario=Usuario(usuario=user,correo=correo,nombre=nombre,apellido=apellido,estado=estado,tipo=tipo,reputacion=0)
            #guarda usuario
            usuario.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta.'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        estadoActivado= EstadosUsuario.objects.get(descripcion='activo')
        usuario= Usuario.objects.get(usuario=user)
        usuario.estado=estadoActivado     
        #Guarda usuario como activo
        usuario.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

'''
def register(request):
    if request.method == 'POST':
        form= UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
        
            user = authenticate(username=username, password= password)
            login(request, user)

            #ver redirect a confirmacion
            #return redirect('')
    else:
        form= UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html',context)

@login_required(login_url='/accounts/login/')
def bussines_profile(request):
    return render(request, 'beautycalendar/bussines_profile.html', {})
'''