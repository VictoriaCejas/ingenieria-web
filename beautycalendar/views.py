from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from .models import Users, ContentUsers,Empleoyees, BeautySalons, WorkItems, WorkingHoursSalons,UserDates, Publications, CommentsPublications, LikesPublications, Reports
from .forms import ContentForm,EmpleoyeesForm, AvatarForm, FrontForm, BeautySalonsForm,BioForm,DatesUserForm, PublicationForm, PublForm, ReportsForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from .decorators import bussines_required
from django.contrib.auth import update_session_auth_hash
from allauth.account.views import PasswordChangeView
from allauth.account.adapter import get_adapter
from allauth.account import signals
from django.views.defaults import page_not_found
from PIL import Image
from django.views.generic import ListView
from datetime import datetime, date, time, timedelta
from .serializers import eventsSerializer,wkHoursSerializer,itemsSelectedSerialezer
from rest_framework import response
from rest_framework.renderers import JSONRenderer
from rest_framework.reverse import reverse


# Create your views here.


def Home(request):
    items= WorkItems.objects.all()
    return render(request, 'beautycalendar/home.html', {'items':items})

def filter_professional(request, pk):
    item= WorkItems.objects.get(id=pk)
    salons= BeautySalons.objects.filter(items=item)
    owners=[]
    for salon in salons:
        owners.append(salon.owner)

    return render(request, 'beautycalendar/filter_professional.html',{'owners':owners})

def Calendar(request,pk):
    salon= Users.objects.get(id=pk)
    services= ContentUsers.objects.filter(user=salon,category=2,state=1)
    services_list= []
    for s in services:
        h= s.attention_time.hour
        m=s.attention_time.minute
        atencion= str(timedelta(hours=h,minutes=m))
        name= s.title+ ' duracion:'+ atencion
        services_list.append((s.id,name),)
    empleoyees= Empleoyees.objects.filter(boss=salon,state=1)
    empleoyees_list=[]
    for e in empleoyees:
        name= e.first_name + ' '+ e.last_name
        empleoyees_list.append((e.id , name),)


    if request.method == 'POST':
        data = dict()
        service= request.POST['services']
        datef= request.POST['date']
        empleoyee= request.POST['empleoyees']
        hours_salon= WorkingHoursSalons.objects.get(salon=salon)
        init= hours_salon.init_time
        finish= hours_salon.finish_time

        serv= ContentUsers.objects.get(id=service)
        serv_tiempo= serv.attention_time
        empl= Empleoyees.objects.get(id=empleoyee)
        disponibles=[]

        from django.utils.dateparse import parse_date
        datef=datetime.strptime(datef, '%d/%m/%Y' )
        t= UserDates.objects.all()
        ocupados= UserDates.objects.filter(date=datef,empleoyee=empleoyee,state=1).order_by('init_time')

        #Calculo huecos
        #huecos[inicio,fin,duracion]
        huecos=[]
        i=0
        last=init
        for turno in ocupados:
            inicio_turno= turno.init_time
            fin_turno= turno.finish_time
            if i==0:
                if inicio_turno.time() != init.time():
                    resta= (timedelta(hours=inicio_turno.hour, minutes=inicio_turno.minute)-timedelta(hours=init.hour,minutes=init.minute)).seconds/3600
                    huecos.append((init,inicio_turno,resta,))
                i=1
                last= fin_turno
            else:

                if inicio_turno.time() != last.time():
                    resta= (timedelta(hours=inicio_turno.hour,minutes=inicio_turno.minute)-timedelta(hours=last.hour,minutes=last.minute)).seconds/3600
                    huecos.append((last,inicio_turno,resta,))
                last=fin_turno

        serv_tiempo_to_hour= int(serv_tiempo.hour)+(int(serv_tiempo.minute))/60
        for h in huecos:
            if serv_tiempo_to_hour <=  h[2]:
                divi= int(h[2]/serv_tiempo_to_hour)
                i=0
                while( i<divi):
                    inicio= (timedelta(hours=h[0].hour, minutes=h[0].minute)) + i * (timedelta(hours=serv_tiempo.hour, minutes=serv_tiempo.minute))
                    h_str=str(inicio)[:-3]
                    disponibles.append((h_str))
                    i=i+1

        serv_tiempo_delta=timedelta(hours=serv_tiempo.hour, minutes=serv_tiempo.minute)

        #Minimo tiempo = 30
        if last.time() != finish.time():
            time= last
            resta= (timedelta(hours=finish.hour,minutes=finish.minute)-timedelta(hours=time.hour,minutes=time.minute)).seconds/3600
            while resta > 0:
                h_str=time.time()
                disponibles.append(h_str)
                time=time+timedelta(minutes=30)
                resta= (timedelta(hours=finish.hour,minutes=finish.minute)-timedelta(hours=time.hour,minutes=time.minute)).seconds/3600
            lista=disponibles

        if disponibles is not None:
            lista= disponibles
        else:
            lista= None

        mycontent= lista
        data['html_time_list'] = render_to_string('beautycalendar/calendar/partial.html', {
            'mycontent': mycontent
        })
        JsonResponse(data)

        form= DatesUserForm(empleoyees_list,services_list, request.POST)
        return render(request,'beautycalendar/calendar/calendar.html',{'form':form,'salon':salon,'mycontent':mycontent})

    else:
        form= DatesUserForm(empleoyees_list, services_list)
        return render(request,'beautycalendar/calendar/calendar.html',{'form':form,'salon':salon})

@login_required
def confirmarTurno(request,pk):

    if request.method == 'POST':
        professional= request.POST['val_professional']
        prf= Empleoyees.objects.get(id=professional)
        service= request.POST['val_service']
        srv= ContentUsers.objects.get(id=service)
        client= request.user
        date= request.POST["nom_day"]
        time= request.POST["nom_time"]
        time=time.split(":")
        h= int(time[0])
        m= int(time[1])
        #time_frm= (h*60)+m
        #att_time= str(datetime.timedelta(minutes=srv.attention_time))

        date=datetime.strptime(date, '%d/%m/%Y' )
        i_time= datetime(year=date.year, month=date.month, day=date.day,hour=h,minute=m)
        att_time=srv.attention_time
        f_time= i_time+ timedelta(hours=att_time.hour, minutes=att_time.minute)

        nuevaCita= UserDates()
        nuevaCita.client= client
        nuevaCita.date= date
        nuevaCita.service= srv
        nuevaCita.empleoyee= prf
        nuevaCita.salon= pk
        nuevaCita.state= 1
        nuevaCita.init_time= i_time
        nuevaCita.finish_time= f_time
        nuevaCita.save()

    return redirect(PrivateProfile)
#    return PrivateProfile(request)
@bussines_required
def getCalendarBussines(request,pk):
    empleoyee= get_object_or_404(Empleoyees,pk=pk)
    return render(request,'beautycalendar/calendar/calendar_bussines.html',{'empleoyee':empleoyee})

@bussines_required
def getEventsBussines(request,pk):

    #Ver lo del serializer
    user=request.user
    empleoyee= get_object_or_404(Empleoyees,pk=pk)

    queryset= UserDates.objects.filter(empleoyee=empleoyee,state=1)
    serializer_data= eventsSerializer(queryset, many=True)
    return JsonResponse( serializer_data.data, safe=False)

@login_required
def getCalendarClient(request):
    return render(request,'beautycalendar/calendar/calendar_client.html',{})

@login_required
def getEventsClient(request):
    user=request.user
    queryset= UserDates.objects.filter(client=user,state=1)
    serialer_data= eventsSerializer(queryset,many=True)
    return JsonResponse(serialer_data.data, safe=False)

@login_required
def listPublication(request):
    user=request.user
    try:
        lista= Publications.objects.filter(owner=user)
        #return render(request,'beautycalendar/calendar/dates.html',{'lista':lista})
    except:
        lista=None
    typeUser=1
    if ('client' in request.path):
        typeUser=2
        
    return render(request,'beautycalendar/publications/publications.html',{'lista':lista,'typeUser':typeUser})

@login_required
def createPublication(request):
    if request.method== 'POST':
        form= PublForm(request.POST, request.FILES)
        if form.is_valid():
            owner= request.user
            publish_date= datetime.now()
            image=form.cleaned_data['imgPublication']
            desc= form.cleaned_data['description']
            publication= Publications(owner=owner,publish_date=publish_date,imagePublication=image,description=desc,)
            publication.save()

            return redirect(listPublication)
    else:
        form= PublForm()
        return render(request,'beautycalendar/publications/publication_create.html',{'form':form})

def getPublication(request,pk):
    if request.method == 'POST':
        form=request.POST
        comment= request.POST['textarea-pub']
        user= request.user
        publication= Publications.objects.get(id=pk)
        date= datetime.now()
        publicationComment= CommentsPublications()
        publicationComment.publication= publication
        publicationComment.date= date
        publicationComment.comment= comment
        publicationComment.user= user
        publicationComment.save()

    publication= Publications.objects.get(id=pk)
    comments= CommentsPublications.objects.filter(publication=publication)
    return render(request,'beautycalendar/publications/publication.html',{'publication':publication, 'comments':comments})

def saveComment(request,pk):

    if request.method == 'POST':
        form=request.POST
        comment= request.POST['textarea-pub']
        user= request.user
        publication= Publications.objects.get(id=pk)
        date= datetime.now()
        publicationComment= CommentsPublications()
        publicationComment.publication= publication
        publicationComment.date= date
        publicationComment.comment= comment
        publicationComment.user= user
        publicationComment.save()

    comments= publicationComment.objects.get(publication=publication)
    return Response(comments)

@login_required
def PrivateProfile(request):

    user= request.user
    myuser= Users.objects.get(email=user.email)
    #kind = Users.objects.get(email=user.email).kind
    kind= myuser.kind

    if kind == 1:
        #bussines
        try:
            items= BeautySalons.objects.filter(owner=myuser)
        except:
            items=""
        return render(request, 'beautycalendar/private_profile_bussines.html', {'usaurio':myuser,'items':items,'user':user})
    elif kind == 2:
        #client
        return render(request, 'beautycalendar/private_profile_client.html', {'usuario': myuser,'user':user})
    else:
        #administrador
        return render(request, 'beautycalendar/private_profile_admin.html', {'usuario': myuser,'user':user})

def DeleteReport(request,pk):
    report = get_object_or_404(Reports, pk=pk)
    data = dict()
    if request.method == 'POST':
        report.delete()
        data['form_is_valid'] = True  
        reports= Reports.objects.all()
        for report in reports:
            inf=Users.objects.get(email=report.informed)    
            report.emailInformed= inf.email
            
            inf=Users.objects.get(email=report.informer)
            report.emailInformer= inf.email
        data['html_report_list'] = render_to_string('beautycalendar/reports/reports_list.html', { 'reports': reports})
    else:
        context = {'report': report}
        data['html_form'] = render_to_string('beautycalendar/reports/partial_report_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
    
def PublicProfile(request, email):
    myuser = Users.objects.get(email=email)
    kind= myuser.kind

    if kind == 1:
        #bussines
        products= ContentUsers.objects.filter(user=myuser,category=1, state=1)
        services= ContentUsers.objects.filter(user=myuser,category=2, state=1)
        empleoyees= Empleoyees.objects.filter(boss=myuser, state=1)
        try:
            items= BeautySalons.objects.filter(owner=myuser)
        except:
            items=""
        return render(request, 'beautycalendar/public_profile_bussines.html', {'myuser':myuser,'items':items,'products':products,'services':services,'empleoyees':empleoyees})
    elif kind == 2:
        #client
        return render(request, 'beautycalendar/public_profile_client.html', {'myuser': myuser})
    else:
        #administrator
        return HttpResponse('Error handler content', status=404)


  #  return render(request, 'beautycalendar/private_profile.html', {'usuario': myuser,'user':user})

def ListReports(request):

    reports= Reports.objects.all()
    for report in reports:
        inf=Users.objects.get(email=report.informed)    
        report.emailInformed= inf.email
        
        inf=Users.objects.get(email=report.informer)
        report.emailInformer= inf.email

    
    return render(request, 'beautycalendar/reports/reports.html', {'reports':reports})


def ListUsersLockes(request):
    users= Users.objects.filter(state=3)
    return render(request, 'beautycalendar/reports/users-locked.html',{'users':users})


def StateUser(request, email, pk=None):
    user= Users.objects.get(email=email)
    data = dict()
   
    if pk is None:
        if request.method == "POST":
            user.state=1
            user.save()
            data['form_is_valid'] = True 
            users= Users.objects.filter(state=3)
            data['html_report_list'] = render_to_string('beautycalendar/reports/users-locked-list.html', {'users': users})
        else:
            context = {'user': user}
            data['html_form'] = render_to_string('beautycalendar/reports/partial_user_unlock.html',
                context,
                request=request,
            )
        
    else:
        
        if request.method == 'POST':
            user.state=3
            user.save()
                
            data['form_is_valid'] = True  # This is just to play along with the existing code
            report= Reports.objects.get(id=pk)
            report.delete()
            reports= Reports.objects.all()
            for report in reports:
                inf=Users.objects.get(email=report.informed)    
                report.emailInformed= inf.email
                
                inf=Users.objects.get(email=report.informer)
                report.emailInformer= inf.email
            data['html_report_list'] = render_to_string('beautycalendar/reports/reports_list.html', {'reports': reports})
        else:
            context = {'user': user,'reportid':pk}
            data['html_form'] = render_to_string('beautycalendar/reports/partial_user_block.html',
                context,
                request=request,
            )
    return JsonResponse(data)
    
    
    
def DeleteEvet(request,pk):
    data=dict()
    event= UserDates.objects.get(pk=pk)
    event.delete()
    data['is_valid']=True
    return JsonResponse(data)



"""CRUD"""
@bussines_required
def mycontent_list(request):
    user= request.user

    if ('products' in request.path):
        mycontent= ContentUsers.objects.filter(user=user,category=1).exclude(state=3)
        return render(request, 'beautycalendar/products/product_list.html', {'mycontent': mycontent})
    if ('services' in request.path):
        mycontent= ContentUsers.objects.filter(user=user,category=2).exclude(state=3)
        return render(request, 'beautycalendar/services/service_list.html', {'mycontent': mycontent})
    if ('empleoyees' in request.path):
        mycontent= Empleoyees.objects.filter(boss=user).exclude(state=3)
        return render(request, 'beautycalendar/empleoyees/empleoyee_list.html', {'mycontent': mycontent})

@bussines_required
def save_mycontent_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            state= request.POST.get("paused", None)
            if state == 'on':
                state=2
            else:
                state=1
            if (('products' in request.path) or ('services' in request.path)):
                if ('products' in request.path):
                    category= 1
                    img = form.cleaned_data['imageProduct']
                    time= None
                if('services' in request.path):
                    category=2
                    img= None
                    time=request.POST.get("attentionTime")
                    time= time.split(':')
                    time= datetime(year=1901,month=1,day=1, hour=int(time[0]), minute=int(time[1]))


                if('update' in request.path):
                    obj = form.save(commit=False)
                    obj.state = state
                    obj.attention_time=time
                    obj.save()
                else:
                    form.save(commit=False)
                    user=request.user
                    title= form.cleaned_data['title']
                    price= form.cleaned_data['price']
                    content= ContentUsers(user=user,category=category,title=title,imageProduct=img,price=price, state=state, attention_time=time)
                    content.save()
                data['form_is_valid'] = True
                mycontent = ContentUsers.objects.filter(user=request.user,category=category).exclude(state=3)
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
                    obj = form.save(commit=False)
                    obj.state= state
                    obj.save()
                #    form.save()
                else:
                    form.save(commit=False)
                    boss= request.user
                    first_name= form.cleaned_data['first_name']
                    last_name= form.cleaned_data['last_name']
                    imageEmpleoyee= form.cleaned_data['imageEmpleoyee']

                    empleoyee= Empleoyees(boss=boss,first_name=first_name,last_name=last_name,imageEmpleoyee=imageEmpleoyee,state=state)
                    empleoyee.save()
                data['form_is_valid'] = True
                mycontent = Empleoyees.objects.filter(boss=request.user).exclude(state=3)
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
    if (('products' in request.path) or ('services' in request.path)):
        if request.method =='POST':
            form = ContentForm(request.POST,request.FILES or None)
        else:
            form = ContentForm()
        if ('products' in request.path):
            return save_mycontent_form(request, form, 'beautycalendar/products/includes/partial_product_create.html')
        if ('services' in request.path):
            return save_mycontent_form(request, form, 'beautycalendar/services/includes/partial_service_create.html')

    if ('empleoyees' in request.path):
        if request.method =='POST':
            form = EmpleoyeesForm(request.POST,request.FILES or None)
        else:
            form = EmpleoyeesForm()
        return save_mycontent_form(request, form, 'beautycalendar/empleoyees/includes/partial_empleoyee_create.html')

@bussines_required
def mycontent_update(request, pk):

    if (('products' in request.path) or ('services' in request.path)):
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
    if (('products' in request.path) or ('services' in request.path)):
        mycontent = get_object_or_404(ContentUsers, pk=pk)
    if ('empleoyees' in request.path):
        mycontent= get_object_or_404(Empleoyees, pk=pk)

    data = dict()
    if request.method == 'POST':
        mycontent.state= 3
        mycontent.save()
        data['form_is_valid'] = True
        if ('products' in request.path):
            mycontent = ContentUsers.objects.filter(user=request.user,category=1).exclude(state=3)
            data['html_product_list'] = render_to_string('beautycalendar/products/includes/partial_product_list.html', {
                'mycontent': mycontent
            })
        if ('services' in request.path):
            mycontent = ContentUsers.objects.filter(user=request.user,category=2).exclude(state=3)
            data['html_service_list'] = render_to_string('beautycalendar/services/includes/partial_service_list.html', {
                'mycontent': mycontent
            })
        if ('empleoyees' in request.path):
            mycontent = Empleoyees.objects.filter(boss=request.user).exclude(state=3)
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

def mycontent_pause(request, pk):
    if (('products' in request.path) or ('services' in request.path)):
        mycontent = get_object_or_404(ContentUsers, pk=pk)
    if ('empleoyees' in request.path):
        mycontent= get_object_or_404(Empleoyees, pk=pk)

    data = dict()

    state= mycontent.state
    if state == 1:
        state= 2
    else:
        state= 1
    mycontent.state= state
    mycontent.save()
    data['form_is_valid'] = True
    if ('products' in request.path):
        mycontent = ContentUsers.objects.filter(user=request.user,category=1).exclude(state=3)
        data['html_product_list'] = render_to_string('beautycalendar/products/includes/partial_product_list.html', {
            'mycontent': mycontent
        })
    if ('services' in request.path):
        mycontent = ContentUsers.objects.filter(user=request.user,category=2).exclude(state=3)
        data['html_service_list'] = render_to_string('beautycalendar/services/includes/partial_service_list.html', {
            'mycontent': mycontent
        })
    if ('empleoyees' in request.path):
        mycontent = Empleoyees.objects.filter(boss=request.user).exclude(state=3)
        data['html_empleoyee_list'] = render_to_string('beautycalendar/empleoyees/includes/partial_empleoyee_list.html', {
            'mycontent': mycontent
        })
    return JsonResponse(data)

@login_required
def avatar_update(request,pk):
    mycontent = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        form= AvatarForm(request.POST, request.FILES, instance=mycontent)
    else:
        if (mycontent== None):
            form= AvatarForm()
        else:
            form= AvatarForm(instance=mycontent)
    return save_my_profile_update_form(request, form, 'beautycalendar/profiles/partial_avatar_update.html')

@login_required
def front_update(request,pk):
    mycontent = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        form= FrontForm(request.POST, request.FILES, instance=mycontent)
    else:
        if (mycontent== None):
            form= FrontForm()
        else:
            form= FrontForm(instance=mycontent)
    return save_my_profile_update_form(request, form, 'beautycalendar/profiles/partial_front_update.html')

@login_required
def bio_update(request,pk):

    mycontent = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        form= BioForm(request.POST, instance= mycontent)
    else:
        if (mycontent== None):
            form= BioForm()
        else:
            form= BioForm(instance=mycontent)

    return save_my_profile_update_form(request, form, 'beautycalendar/profiles/partial_bio_update.html')

def get_HoursandDays(request):

    user=request.user
    queryset= get_object_or_404(WorkingHoursSalons,salon=user)
    if queryset:
        serialer_data= wkHoursSerializer(queryset,many=False)

    return JsonResponse(serialer_data.data, safe=False)

def get_items(request):
    user=request.user
    querysey= BeautySalons.objects.filter(owner=user)
    serialer_data= itemsSelectedSerialezer(querysey, many=True)
    return JsonResponse(serialer_data.data, safe=False)

def save_my_profile_update_form(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            data['form_is_valid'] = True
            user= Users.objects.get(email=request.user)

            if ('avatar' in request.path):
                image=form.cleaned_data['imageAvatar']
                if (image is False):
                    image= None
                user.imageAvatar= image

            if ('front' in request.path):
                image=form.cleaned_data['imageFront']
                if (image is False):
                    image= None
                user.imageFront= image

            if ('bio' in request.path):
                if user.kind==1:
                    name=form.cleaned_data['name_salon']
                    user.name_salon= name
                else:
                    name= form.cleaned_data['first_name']
                    user.first_name= name
                user.description= form.cleaned_data['description']
                items= form.cleaned_data['items']
                delete= BeautySalons.objects.filter(owner=request.user).delete()
                for i in items:
                    try:
                        salon= BeautySalons.objects.get(owner=request.user,items=i)
                    except:
                        salon= BeautySalons(owner= request.user, items= i)
                        salon.save()
                ihour=request.POST['initHour']
                fhour=request.POST['endHour']
                ihour=ihour.split(':')
                fhour=fhour.split(':')
                initDay= request.POST['initDay']
                endDay= request.POST['endDay']
                initHour= datetime(year=1901,month=1,day=1,hour=int(ihour[0]),minute=int(ihour[1]))
                endHour= datetime(year=1901,month=1,day=1,hour=int(fhour[0]),minute=int(fhour[1]))
                salon=user
                try:
                    timeExist = WorkingHoursSalons.objects.get(salon=salon)
                    timeExist.delete()
                    times = WorkingHoursSalons(salon=salon,init_date=initDay,finish_date=endDay,init_time=initHour,finish_time=endHour)

                except:
                    times = WorkingHoursSalons(salon=salon,init_date=initDay,finish_date=endDay,init_time=initHour,finish_time=endHour)
                finally:
                    times.save()
            user.save()

            usuario=user
            if (user.kind == 1):
                data['html_profile'] = render_to_string('beautycalendar/private_profile_bussines.html', {'user':user})
            if (user.kind== 2):
                data['html_profile'] = render_to_string('beautycalendar/private_profile_client.html', {'user':user})
            if (user.kind== 3):
                data['html_profile'] = render_to_string('beautycalendar/private_profile_admin.html', {'user':user})

        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def facebookprivacy(request):

    return render(request,'allauth/socialaccount/privacy.html')

class MyPasswordChangeView(PasswordChangeView):
    """
    Custom class to override the password change view
    """

    success_url = "/private_profile"

    # Override form valid view to keep user logged i
    def form_valid(self, form):

        form.save()

        # Update session to keep user logged in.
        update_session_auth_hash(self.request, form.user)

        get_adapter().add_message(self.request,
                                            messages.SUCCESS,
                                            'account/messages/password_changed.txt')

        signals.password_changed.send(sender=self.request.user.__class__,
                                            request=self.request,
                                            user=self.request.user)

        return super(PasswordChangeView, self).form_valid(form)

password_change = login_required(MyPasswordChangeView.as_view())


def save_report(request,form,template_name,email):
    data=dict()

    if request.method=='POST':
        if form.is_valid():
            data['form_is_valid'] = True
            form.save(commit=False)
            informer= request.user.emaillike
            informed= email
            option= request.POST['options']
            other= request.POST['other']
            report= Reports()
            report.informer= informer
            report.informed= informed
            report.options= option
            report.other= other
            report.save()
        user=request.user
        data['html_profile'] = render_to_string('beautycalendar/private_profile_client.html', {'user':user})
        # return redirect(PrivateProfile)
    else:
        context = {'form': form,'email':email}
        data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)



def reporter(request,email):
    if request.method == 'POST':
        form= ReportsForm(request.POST)
    else:
        form= ReportsForm()

    return save_report(request, form, 'beautycalendar/profiles/partial_report.html',email)



    
def Like(request,pk):
    data= dict()
    user=request.user
    publ=Publications(pk=pk)
    
    try:
        publication= LikesPublications.objects.get(user=user,publication=publ)
        if ('dislike' in request.path):
            if (publication.value == False):
                data['is_valid']=False
            else:
                publication.value= False
                data['is_valid']=True
                publication.save()
        else:
            if (publication.value == True):
                data['is_valid']= False
            else:
                publication.value= True
                data['is_valid']=True
                publication.save()     
    except:
            newLike= LikesPublications()
            newLike.user=user
            newLike.publication=publ
            if ('dislike' in request.path):
                newLike.valur= False
            else:
                newLike.value= True
            newLike.save()
            data['is_valid']=True
        
    return JsonResponse(data)

def DeletePublication(request, pk):
    data=dict()
    publication= Publications.objects.get(pk=pk)
    publication.delete()
    data['is_valid']=True
    return JsonResponse(data)
    
def TotalLikes(request, pk):
    
    data= dict()
    user=request.user
    publication= Publications(pk=pk)
    likes= LikesPublications.objects.filter(user=user,publication=publication) 
    positives=0
    negatives=0
    for l in likes:
        if l.value== True:
            positives = positives + 1
        else:
            negatives = negatives + 1
    data['positives']=positives
    data['negatives']= negatives
    
    return JsonResponse(data)
    
    
def mi_error_404(request,Exception):
    nombre_template = 'beautycalendar/404.html'
    return page_not_found(request, template_name=nombre_template)

