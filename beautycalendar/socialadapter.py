from .models import MyUser
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse
from allauth.account.utils import perform_login


class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        if user.id:  
            return          
        try:
            myuser = MyUser.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'                
            perform_login(request, myuser, 'none')
        except MyUser.DoesNotExist:
            pass