from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import User, ContentUser
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContentForm
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
    myuser= User.objects.get(email=user.email)
    kind = User.objects.get(email=user.email).kind
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



""""""
def mycontent_list(request):
    user= request.user
    if ('products' in request.path):
        mycontent= ContentUser.objects.filter(user=user,category=1)
        return render(request, 'beautycalendar/product_list.html', {'mycontent': mycontent})
    if ('services' in request.path):
        mycontent= ContentUser.objects.filter(user=user,category=2)
        return render(request, 'beautycalendar/service_list.html', {'mycontent': mycontent})

def save_mycontent_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():     
            if ('products' in request.path):
                category= 1
                img = form.cleaned_data['imageProduct']
            if('services' in request.path):
                category=2
                img= None       
            
            if('update' in request.path):
                import web_pdb; web_pdb.set_trace()
                form.save()
            else:
                form.save(commit=False)            
                user=request.user
                title= form.cleaned_data['title']
                price= form.cleaned_data['price']    
                content= ContentUser(user=user,category=category,title=title,imageProduct=img,price=price)
                content.save()
            data['form_is_valid'] = True
            mycontent = ContentUser.objects.filter(user=request.user,category=category)
            if ('products' in request.path):
                data['html_product_list'] = render_to_string('beautycalendar/includes/partial_product_list.html', {
                    'mycontent': mycontent
                })
            if ('services' in request.path):
                data['html_service_list'] = render_to_string('beautycalendar/includes/partial_service_list.html', {
                    'mycontent': mycontent
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def mycontent_create(request):

    if request.method =='POST':
        form = ContentForm(request.POST,request.FILES or None)
    else:
        form = ContentForm()
    if ('products' in request.path):
        return save_mycontent_form(request, form, 'beautycalendar/includes/partial_product_create.html')
    if ('services' in request.path):
        return save_mycontent_form(request, form, 'beautycalendar/includes/partial_service_create.html')

def mycontent_update(request, pk):
    mycontent = get_object_or_404(ContentUser, pk=pk)
   
    if request.method == 'POST':  
        if ('products' in request.path):  
            form = ContentForm(request.POST,request.FILES, instance=mycontent)
        if ('services' in request.path):
            form = ContentForm(request.POST,request.FILES, instance=mycontent)
            
    else:
        form = ContentForm(instance=mycontent)

    if ('products' in request.path):
        return save_mycontent_form(request, form, 'beautycalendar/includes/partial_product_update.html')
    if ('services' in request.path):
        return save_mycontent_form(request, form, 'beautycalendar/includes/partial_service_update.html')
        

def mycontent_delete(request, pk):
    mycontent = get_object_or_404(ContentUser, pk=pk)
    data = dict()
    if request.method == 'POST':
        #import web_pdb; web_pdb.set_trace()
        mycontent.delete()
        data['form_is_valid'] = True
        #mycontent = ContentUser.objects.all()
        if ('products' in request.path):
            mycontent = ContentUser.objects.filter(user=request.user,category=1)        
            data['html_product_list'] = render_to_string('beautycalendar/includes/partial_product_list.html', {
                'mycontent': mycontent
            })
        if ('services' in request.path):
            mycontent = ContentUser.objects.filter(user=request.user,category=2)        
            data['html_service_list'] = render_to_string('beautycalendar/includes/partial_service_list.html', {
                'mycontent': mycontent
            })
    else:
        context = {'mycontent': mycontent}
        if ('products' in request.path):
            data['html_form'] = render_to_string('beautycalendar/includes/partial_product_delete.html', context, request=request)
        if ('services' in request.path):
            data['html_form'] = render_to_string('beautycalendar/includes/partial_service_delete.html', context, request=request)
            
    return JsonResponse(data)