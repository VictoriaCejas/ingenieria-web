from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Users, ContentUsers,Empleoyees
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContentForm,EmpleoyeesForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView, View, DeleteView
from django.http import JsonResponse
from django.template.loader import render_to_string
from .decorators import bussines_required
# Create your views here.


def Home(request):
    return render(request, 'beautycalendar/home.html', {})
 
    
@login_required(login_url='/accounts/login/')
def Private(request):
    return render(request, 'beautycalendar/privado.html', {})


def Public(request):
    return render(request, 'beautycalendar/publico.html', {})


@login_required
def PrivateProfile(request):
    
    user= request.user
    myuser= Users.objects.get(email=user.email)
    kind = Users.objects.get(email=user.email).kind
    if request.method=="POST":
        pass
    else:
        """
        Es un GET
        """
        pass

    if kind == 1:
        #bussines  
        #products= ContentUser.objects.filter(user=user,category=1)
        return render(request, 'beautycalendar/private_profile_bussines.html', {})
    elif kind == 2:
        #client
        return render(request, 'beautycalendar/private_profile_client.html', {'usuario': myuser,'user':user})
    else:
        #administrator
        return render(request, 'beautycalendar/private_profile_admin.html', {'usuario': myuser,'user':user})

  #  return render(request, 'beautycalendar/private_profile.html', {'usuario': myuser,'user':user})



def PublicProfile(request):
    pass


"""CRUD"""
@bussines_required
def mycontent_list(request):
    user= request.user
    if ('products' in request.path):
        mycontent= ContentUsers.objects.filter(user=user,category=1)
        return render(request, 'beautycalendar/products/product_list.html', {'mycontent': mycontent})
    if ('services' in request.path):
        mycontent= ContentUsers.objects.filter(user=user,category=2)
        return render(request, 'beautycalendar/services/service_list.html', {'mycontent': mycontent})
    if ('empleoyees' in request.path):
        mycontent= Empleoyees.objects.filter(boss=user)
        return render(request, 'beautycalendar/empleoyees/empleoyee_list.html', {'mycontent': mycontent})
        
@bussines_required
def save_mycontent_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():   
            #import web_pdb; web_pdb.set_trace()
            if (('products' or 'services') in request.path):  
                if ('products' in request.path):
                    category= 1
                    img = form.cleaned_data['imageProduct']
                if('services' in request.path):
                    category=2
                    img= None       
                
                if('update' in request.path):
                    form.save()
                else:
                    form.save(commit=False)            
                    user=request.user
                    title= form.cleaned_data['title']
                    price= form.cleaned_data['price']    
                    content= ContentUsers(user=user,category=category,title=title,imageProduct=img,price=price)
                    content.save()
                data['form_is_valid'] = True
                mycontent = ContentUsers.objects.filter(user=request.user,category=category)
                if ('products' in request.path):
                    data['html_product_list'] = render_to_string('beautycalendar/products/includes/partial_product_list.html', {
                        'mycontent': mycontent
                    })
                if ('services' in request.path):
                    data['html_service_list'] = render_to_string('beautycalendar/services/includes/partial_service_list.html', {
                        'mycontent': mycontent
                    })
            if ('empleoyees' in request.path):
                if('update' in request.path):
                    form.save()
                else:
                    form.save(commit=False)
                   # import web_pdb; web_pdb.set_trace()
                    boss= request.user
                    first_name= form.cleaned_data['first_name']
                    last_name= form.cleaned_data['last_name']
                    imageEmpleoyee= form.cleaned_data['imageEmpleoyee']
                    empleoyee= Empleoyees(boss=boss,first_name=first_name,last_name=last_name,imageEmpleoyee=imageEmpleoyee)
                    empleoyee.save()
                data['form_is_valid'] = True
                mycontent = Empleoyees.objects.filter(boss=request.user)
                data['html_empleoyee_list'] = render_to_string('beautycalendar/empleoyees/includes/partial_empleoyee_list.html', {
                    'mycontent': mycontent
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@bussines_required
def mycontent_create(request):
    if (('products' or 'services') in request.path):
        if request.method =='POST':
            form = ContentForm(request.POST,request.FILES or None)
        else:
            form = ContentForm()
        
        if ('products' in request.path):
            return save_mycontent_form(request, form, 'beautycalendar/products/includes/partial_product_create.html')
        if ('services' in request.path):
            return save_mycontent_form(request, form, 'beautycalendar/services/includes/partial_service_create.html')
    
    if ('empleoyees' in request.path):
        #import web_pdb; web_pdb.set_trace()
        if request.method =='POST':
            form = EmpleoyeesForm(request.POST,request.FILES or None)
        else:
            form = EmpleoyeesForm()
        return save_mycontent_form(request, form, 'beautycalendar/empleoyees/includes/partial_empleoyee_create.html')

@bussines_required
def mycontent_update(request, pk):
    
    if (('products' or 'services') in request.path):
        mycontent = get_object_or_404(ContentUsers, pk=pk)
        if request.method == 'POST':  
            form = ContentForm(request.POST,request.FILES, instance=mycontent)
        else:
            form = ContentForm(instance=mycontent)

        if ('products' in request.path):
            return save_mycontent_form(request, form, 'beautycalendar/products/includes/partial_product_update.html')
        if ('services' in request.path):
            return save_mycontent_form(request, form, 'beautycalendar/services/includes/partial_service_update.html')
    
    if ('empleoyees' in request.path):
        mycontent=get_object_or_404(Empleoyees,pk=pk)
        if request.method == 'POST':  
                form= EmpleoyeesForm(request.POST, request.FILES, instance=mycontent)
        else:
                form= EmpleoyeesForm(instance=mycontent)
        return save_mycontent_form(request, form, 'beautycalendar/empleoyees/includes/partial_empleoyee_update.html')

@bussines_required
def mycontent_delete(request, pk):
    if (('products' or 'services') in request.path):
        mycontent = get_object_or_404(ContentUsers, pk=pk)
    if ('empleoyees' in request.path):
        mycontent= get_object_or_404(Empleoyees, pk=pk)
    
    data = dict()
    if request.method == 'POST':
        #import web_pdb; web_pdb.set_trace()
        mycontent.delete()
        data['form_is_valid'] = True
        #mycontent = ContentUser.objects.all()
        if ('products' in request.path):
            mycontent = ContentUsers.objects.filter(user=request.user,category=1)        
            data['html_product_list'] = render_to_string('beautycalendar/products/includes/partial_product_list.html', {
                'mycontent': mycontent
            })
        if ('services' in request.path):
            mycontent = ContentUsers.objects.filter(user=request.user,category=2)        
            data['html_service_list'] = render_to_string('beautycalendar/services/includes/partial_service_list.html', {
                'mycontent': mycontent
            })
        if ('empleoyees' in request.path):
            mycontent = Empleoyees.objects.filter(boss=request.user)        
            data['html_empleoyee_list'] = render_to_string('beautycalendar/empleoyees/includes/partial_empleoyee_list.html', {
                'mycontent': mycontent
            })
    
    else:
        context = {'mycontent': mycontent}
        if ('products' in request.path):
            data['html_form'] = render_to_string('beautycalendar/products/includes/partial_product_delete.html', context, request=request)
        if ('services' in request.path):
            data['html_form'] = render_to_string('beautycalendar/services/includes/partial_service_delete.html', context, request=request)
        if ('empleoyees' in request.path):
            data['html_form'] = render_to_string('beautycalendar/empleoyees/includes/partial_empleoyee_delete.html', context, request=request)
            
    return JsonResponse(data)

""""""

def facebookprivacy(request):

    return render(request,'allauth/socialaccount/privacy.html')