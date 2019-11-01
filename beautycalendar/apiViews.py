from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework import viewsets
from beautycalendar.serializers import serviceSerializer, bussineSerializer, productSerializer, tokenSerializer, userSerializer, eventsSerializer
from beautycalendar.models import Users, ContentUsers, UserDates, Empleoyees
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from rest_framework import generics
from django.http import JsonResponse
from datetime import datetime, date, time, timedelta
from allauth.socialaccount.models import SocialToken
import json

def getUser(email):
    return Users.objects.get(email=email)

class UserView(viewsets.ReadOnlyModelViewSet):
    '''Lista usuarios
    Devuelve un usuario por id'''
    queryset=Users.objects.all()
    serializer_class= userSerializer
    
class tokenAppView(APIView):
    'obtiene token del provider para un usuario para utilizar GoogleLogin y FacebookLogin'
    def post(self,request):
        import web_pdb; web_pdb.set_trace()    
        data=json.loads(request.body)    
        email=data['email']
        provider=data['provider']
        user= getUser(email)
        token=SocialToken.objects.filter(account__user=user, account__provider=provider).values('token')
        data=dict()
        data['tokenApp']=token
        return Response(data=data)
        
class ServiceList(generics.ListAPIView):
    '''Lista servicios por usuario recibiendo email en json'''
    serializer_class= serviceSerializer
    
    def get_queryset(self):
        import web_pdb; web_pdb.set_trace()
        email=self.kwargs['email']
        user= Users.objects.get(email=email)
        services= ContentUsers.objects.filter(state=1,category=2,user=user)
        serializer= serviceSerializer(services,many=True)
        return JsonResponse(serializer,safe=False)
    
class ServicesView(APIView):
    '''Permite postear un nuevo servicio si es usuario bussines'''
    serializer_class=serviceSerializer
    
    def post(self,request):
        user= request.user
        data=json.loads(request.body)
        salon=data['user']
        # salon=request.POST['user']
        try:
            userSalon= Users.objects.get(id=salon)
        except:
            userSalon= Users.objects.get(email=salon)

        if user==userSalon:
            if user.kind == 1:
                title= data['title']
                price=data['price']

                time=data['attention_time']
                time= time.split(' ')
                time=time[1].split(':')
                time= datetime(year=1901,month=1,day=1, hour=int(time[0]), minute=int(time[1]))
                service= ContentUsers()
                service.user=user
                service.category=2
                service.state=1
                service.title=title
                service.attention_time=time
                service.price=price
                service.save()
                serializer= serviceSerializer(service,many=False)
                return JsonResponse(serializer.data,safe=False)

            else:
                return Response(data={'usuario no es bussines'})
        else:
            return Response(data={'No puede modificar un usuario distinto al suyo'}) 

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView):
    """Google OAuth login endpoint

    POST parameter `code` should contain the access code provided by Google OAuth backend,
    which the backend uses in turn to fetch user data from the Google authentication backend.

    POST parameter `access_token` might not function with this function.

    Requires `callback_url` to be properly set in the configuration, this is of format:

        callback_url = https://{domain}/accounts/google/login/callback/
        
    Recibe parametros, no JSON
    """

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url= ['http://127.0.0.1:8000/accounts/google/login/callback']

class DatesClientView(APIView):
    '''Lista los turnos para un cliente pasando en json email
    '''  
    permission_classes = (IsAuthenticated,)             
    def get(self,request, *args, **kwargs):
        import web_pdb; web_pdb.set_trace()
        data=json.loads(request.body)
        email= data['email']
        client=Users.objects.get(email=email)
        dates= UserDates.objects.filter(client=client)
        serializer=eventsSerializer(dates,many=True)
        return JsonResponse(serializer.data,safe=False)
    
        