from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Users, ContentUsers, Empleoyees
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, UserForm
from allauth.account.signals import email_confirmed, user_signed_up
from django.dispatch import receiver
from allauth.account.adapter import DefaultAccountAdapter


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    Choices = [('bussines', 'Bussines')]
    bussines = forms.BooleanField(required=False, initial=False, label='Bussines', help_text='Cuenta para emprendedor',)

    #class Meta:
     #   model=User
      #  fields=['bussines']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class ContentForm(forms.ModelForm):
    
    class Meta:
        model = ContentUsers
        fields = ['user','category','title','imageProduct','price']
        widgets = {'user':forms.HiddenInput(),'category':forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['user'].required= False
        self.fields['category'].required= False

class EmpleoyeesForm(forms.ModelForm):

    class Meta:
        model= Empleoyees
        fields= ['boss','first_name','last_name','imageEmpleoyee']
        widgets= {'boss':forms.HiddenInput(),}
   
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['boss'].required= False
    
class AvatarForm(forms.ModelForm):
    
    class Meta:
        model=Users
        fields=['imageAvatar']

class FrontForm(forms.ModelForm):
    class Meta:
        model= Users
        fields=['imageFront']
