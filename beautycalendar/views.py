from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Usuario, Tipo_Usuario, Estado_Usuario

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